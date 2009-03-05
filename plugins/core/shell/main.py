#-*- coding: utf8 -*
#
# Max E. Kuznecov <syhpoon@syhpoon.name> 2009
#

import sys
import termios
import os
import pty
import signal
import struct
import fcntl
import tty

from libxyz.core.plugins import BasePlugin

class XYZPlugin(BasePlugin):
    "Plugin shell"

    NAME = u"shell"
    AUTHOR = u"Max E. Kuznecov <syhpoon@syhpoon.name>"
    VERSION = u"0.1"
    BRIEF_DESCRIPTION = u"Shell wrapper"
    FULL_DESCRIPTION = u"Execute commands in external shell"
    NAMESPACE = u"core"
    MIN_XYZ_VERSION = None
    DOC = None
    HOMEPAGE = "http://xyzcmd.syhpoon.name"

    shell_args = {"sh": ["-c"],
                  "bash": ["-c"],
                  "zsh": ["-c"]
                  }

    def __init__(self, xyz):
        
        super(XYZPlugin, self).__init__(xyz)

        self.export(self.execute)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def prepare(self):
        # Determine shell

        shell = os.getenv("SHELL")

        if not shell:
            shell = "/bin/sh"

        _shell = os.path.basename(shell)

        if _shell not in self.shell_args:
            shell, _shell = "/bin/sh", "sh"

        self.shell = [shell] + self.shell_args[_shell]
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def execute(self, cmd):
        """
        Execute command in shell
        """

        self.xyz.screen.clear()
        stdin = sys.stdin.fileno()
        stdout = sys.stdout
        current = termios.tcgetattr(stdin)
        termios.tcsetattr(stdin, termios.TCSADRAIN, self.xyz.term)
        #TODO: make it more portable!
        stdout.write("\x1b[H\x1b[2J")

        stdout.write("%s%s\n" %
                     (self.xyz.conf[u"plugins"][":sys:cmd"][u"prompt"],
                      cmd))
        stdout.flush()
            
        winsize = fcntl.ioctl(stdout.fileno(), termios.TIOCGWINSZ, '1234')

        pid, fd = pty.fork()

        # Child - Exec passed cmd
        if pid == 0:
            # Restore window size
            fcntl.ioctl(stdout.fileno(), termios.TIOCSWINSZ, winsize)
            os.execvp(self.shell[0], self.shell + [cmd])

            # WTF?
            sys.exit()
        # Parent - Fork. In child redirect stdin > pty child.
        # In parent redirect pty child > stdout
        else:
            child = os.fdopen(fd, "r+")

            xpid = os.fork()

            if xpid == 0:
                tty.setcbreak(stdin)

                while True:
                    try:
                        line = os.read(stdin, 1024)

                        if not line:
                            break

                        child.write(line)
                        child.flush()
                    except Exception:
                        break

                sys.exit()
            else:
                while True:
                    try:
                        line = os.read(child.fileno(), 1024)

                        if not line:
                            break

                        stdout.write(line)
                        stdout.flush()
                    except Exception:
                        break

            os.kill(xpid, signal.SIGTERM)
            raw_input(_(u"Press RETURN to continue..."))
            termios.tcsetattr(stdin, termios.TCSADRAIN, current)
