#-*- coding: utf8 -*
#
# Author <e-mail> year
#

from libxyz.core.plugins import BasePlugin

class XYZPlugin(BasePlugin):
    "Plugin logger"

    NAME = u"logger"
    AUTHOR = u"Max E. Kuznecov ~syhpoon <mek@mek.uz.ua>"
    VERSION = u"0.1"
    BRIEF_DESCRIPTION = u"Logger console"
    FULL_DESCRIPTION = u"Logger console is used to collect system messages."
    NAMESPACE = u"core"

    DOC = u"There are several message levels:\n"\
          u"ERROR: Critical error. Program must be closed.\n"\
          u"WARNING: Non-critical warning.\n"\
          u"INFO: Informational message.\n"\
          u"DEBUG: Debug messages.\n"\
          u"Plugin configuration:\n"\
          u"levels - a list of levels to track "

    def __init__(self, xyz):
        super(XYZPlugin, self).__init__(xyz)

        self.public = {"show_console": self._show_console}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def prepare(self):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def finalize(self):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _show_console(self):
        """
        show_console
        """

        pass
