#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
#

from libxyz.core.plugin import BasePlugin
from libxyz.ui import MessageBox
from libxyz.version import Version

class XYZPlugin(BasePlugin):
    """
    Example plugin
    """

    # AUTHOR: Author name

    AUTHOR = u"Max E. Kuznecov ~syhpoon <mek@mek.uz.ua>"

    # VERSION: Plugin version

    VERSION = "0.1"

    # Brief one line description

    BRIEF_DESCRIPTION = u"Simple hello plugin"

    # Full plugin description

    FULL_DESCRIPTION = u"Hello plugin is an example of XYZCommander plugin."\
                       u"It shows main aspects of plugin creation."\
                       u"Functionality is limited to single method: SayHello "\
                       u"which shows greeting message box."

    # NAMESPACE: Plugin namespace. For detailed information about
    #            namespaces see Plugins chapter of XYZCommander user manual.
    #            Full namespace path to method is:
    #            xyz:plugins:misc:hello:SayHello

    NAMESPACE = "misc"

    def __init__(self, xyz):
        self.xyz = xyz
        self.public[u"SayHello"] = self._say_hello

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _say_hello(self):
        """
        Exported method
        Shows simple greeting dialog
        """

        _msg = self.FULL_DESCRIPTION
        _title = u"XYZCommander version %s" % Version.version

        _box = MessageBox(self.xyz.screen, _msg, _title)
        self.xyz.screen.draw_screen(_dim, _box.render(_dim, True))

        return self.xyz.screen.get_input()
