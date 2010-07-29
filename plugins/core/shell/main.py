#-*- coding: utf8 -*
#
# Max E. Kuznecov <syhpoon@syhpoon.name> 2009
#

import sys
import errno
import os
import signal

import libxyz.core as core

from libxyz.core.utils import bstring
from libxyz.core.plugins import BasePlugin

from bash import bash_setup

class XYZPlugin(BasePlugin):
    "Shell plugin"

    NAME = u"shell"
    AUTHOR = u"Max E. Kuznecov <syhpoon@syhpoon.name>"
    VERSION = u"0.2"
    BRIEF_DESCRIPTION = _(u"Shell wrapper")
    FULL_DESCRIPTION = _(u"Execute commands in external shell")
    NAMESPACE = u"core"
    MIN_XYZ_VERSION = None
    DOC = u"Configuration variables:\n"\
          u"wait - Boolean flag indicating whether to wait for user pressing "\
          u"key after command executed. Default True\n"\
          u"setup_shell - Boolean flag indicating whether to run "\
          u"system shell-specific initialization. Default True"

    HOMEPAGE = "http://xyzcmd.syhpoon.name"
    EVENTS = [("execute",
               _(u"Fires before command execution. "\
                 u"Arguments: a command to be executed")),
              ]
    
    shell_args = {
        "sh": ["-c"],
        "bash": ["-c"],
        "zsh": ["-c"]
        }

    shell_setup = {
        "bash": bash_setup
        }

    def __init__(self, xyz):
        self.status = 0
        self.shell = None

        super(XYZPlugin, self).__init__(xyz)

        self.export(self.execute)
        self.export(self.echo)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def prepare(self):
        # Determine shell
        shell = self.xyz.conf["xyz"]["shell"]
        _base = os.path.basename(shell)

        if _base not in self.shell_args:
            shell, _base = "/bin/sh", "sh"

        self.shell = [shell] + self.shell_args[_base]

        # Setup shell
        if self.conf["setup_shell"] and _base in self.shell_setup:
            self.shell_setup[_base](shell)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def execute(self, cmd, wait=None):
        """
        Execute command in shell
        """

        cmd = bstring(cmd)
        self.fire_event("execute", cmd)

        def _exec():
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
                    except KeyboardInterrupt:
                        pass
                    except OSError, e:
                        if e.errno != errno.EINTR:
                            break

            return self.status

        return self._exec_engine(cmd, _exec, wait)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def echo(self, msg):
        """
        Echo a message to terminal output
        """

        def _echo():
            print(msg)
        
        return self._exec_engine("echo", _echo)
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _press_key(self, msg, key):
        """
        Print prompt and wait for the key to be pressed
        """

        sys.stdout.write(bstring(msg))
        sys.stdout.flush()
        
        while True:
            try:
                m = os.read(sys.stdin.fileno(), 1024)
                if key in m:
                    break
            except OSError, e:
                if e.errno != errno.EINTR:
                    break

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _exec_engine(self, cmd, cmdf, wait=None):
        """
        Execute command engine
        """

        self.xyz.screen.clear()
        stdout = sys.stdout
        self.xyz.screen.stop()

        _current_term = None
        
        # Restore original terminal settings
        if self.xyz.term is not None:
            _current_term = core.utils.term_settings()[-1]
            core.utils.restore_term(self.xyz.term)
        
        # Clear the screen
        #TODO: make it more portable!
        stdout.write("\x1b[H\x1b[2J")

        stdout.write("%s%s\n" %
                     (bstring(
                         self.xyz.conf[u"plugins"][":sys:cmd"][u"prompt"]),
                      cmd))
        stdout.flush()

        def _sigwinch(_a, _b):
            self.xyz.screen.resized = True

        signal.signal(signal.SIGWINCH, _sigwinch)

        status = cmdf()
        
        if _current_term is not None:
            core.utils.restore_term(_current_term)

        if wait == True or (wait != False and self.conf["wait"]):
            self._press_key(_(u"Press ENTER to continue..."), "\n")

        self.xyz.screen.start()

        return status
