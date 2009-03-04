#-*- coding: utf8 -*
#
# Max E. Kuznecov <syhpoon@syhpoon.name> 2009
#

import sys
import termios
import os
import pty
import signal

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

    def __init__(self, xyz):
        super(XYZPlugin, self).__init__(xyz)

        self.export(self.execute)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def execute(self, cmd):
        """
        Execute command in shell
        """

        self.xyz.screen.clear()
        stdin = sys.stdin.fileno()
        current = termios.tcgetattr(stdin)
        #TODO: savedterm!
        termios.tcsetattr(stdin, termios.TCSADRAIN, savedterm)
        #TODO: make it more portable!
        sys.stdout.write("\x1b[H\x1b[2J")

        sys.stdout.write("%s%s\n" %
                         (self.xyz.conf[u"plugins"][":sys:cmd"][u"prompt"],
                          cmd))
        sys.stdout.flush()
            
        pid, fd = pty.fork()

        # Child
        if pid == 0:
            # TODO: actual user shell
            os.execvp("/usr/local/bin/zsh",
                      ["/usr/local/bin/zsh", "-c", cmd])

            # WTF?
            sys.exit()
        # Parent
        else:
            child = os.fdopen(fd, "r+")

            xpid = os.fork()

            if xpid == 0:
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

                        sys.stdout.write(line)
                        sys.stdout.flush()
                    except Exception:
                        break

            os.kill(xpid, signal.SIGTERM)
            raw_input("Press RETURN to continue...")
            termios.tcsetattr(stdin, termios.TCSADRAIN, current)
