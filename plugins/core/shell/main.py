#-*- coding: utf8 -*
#
# Max E. Kuznecov <syhpoon@syhpoon.name> 2009
#

import sys
import errno
import os
import signal

from libxyz.core.utils import bstring
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
        self.status = 0
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
        stdout = sys.stdout
        self.xyz.screen.stop()
        #TODO: make it more portable!
        stdout.write("\x1b[H\x1b[2J")

        stdout.write("%s%s\n" %
                     (bstring(
                         self.xyz.conf[u"plugins"][":sys:cmd"][u"prompt"]),
                      cmd))
        stdout.flush()

        def _sigwinch(sig, frame):
            self.xyz.screen.resized = True
            
        signal.signal(signal.SIGWINCH, _sigwinch)

        pid = os.fork()

        # Child - Exec passed cmd
        if pid == 0:
            os.execvp(self.shell[0], self.shell + [cmd])
            # WTF?
            sys.exit()
        # Parent
        else:
            while True:
                try:
                    self.status = os.waitpid(pid, 0)
                except OSError, e:
                    if e.errno != errno.EINTR:
                        break

        self._press_key(_(u"Press ENTER to continue..."), "\n")
        self.xyz.screen.start()

        return self.status

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _press_key(self, msg, key):
        """
        Print prompt and wait for the key to be pressed
        """

        sys.stdout.write(msg)
        sys.stdout.flush()
        
        while True:
            try:
                m = os.read(sys.stdin.fileno(), 1024)
                if key in m:
                    break
            except OSError, e:
                if e.errno != errno.EINTR:
                    break
