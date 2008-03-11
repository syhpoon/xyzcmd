#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
#

from libxyz.core.plugin import BasePlugin
from libxyz.ui import MessageBox
from libxyz.version import Version

class Hello(BasePlugin):
    """
    Example plugin
    """

    def __init__(self, xyz):
        self.xyz = xyz
        self.public[u"SayHello"] = self._say_hello

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _say_hello(self):
        """
        Exported method
        Shows simple greeting dialog
        """

        _msg = u""
        _title = u"XYZCommander v %s" % Version.version

        _box = MessageBox(self.xyz.screen, _msg, _title)
        self.xyz.screen.draw_screen(_dim, _box.render(_dim, True))

        return self.xyz.screen.get_input()
