#-*- coding: utf8 -*
#
# Max E. Kuznecov <syhpoon@syhpoon.name> 2008
#

from libxyz.ui import lowui
from libxyz import Version

import libxyz.ui as uilib
import libxyz.const

from libxyz.core.plugins import BasePlugin

class XYZPlugin(BasePlugin):
    "Plugin about"

    NAME = u"about"
    AUTHOR = u"Max E. Kuznecov <syhpoon@syhpoon.name>"
    VERSION = u"0.1"
    BRIEF_DESCRIPTION = u"About plugin"
    FULL_DESCRIPTION = u""
    NAMESPACE = u"misc"
    MIN_XYZ_VERSION = None
    DOC = None
    HOMEPAGE = u"xyzcmd.syhpoon.name"

    def __init__(self, xyz):
        super(XYZPlugin, self).__init__(xyz)

        self.public = {u"show_box": self.show_box}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def show_box(self):
        """
        Show About box
        """

        _font6x6 = lowui.Thin6x6Font()
        _font3x3 = lowui.Thin3x3Font()
        _attr = self.xyz.skin.attr(uilib.Box.resolution, u"box")

        _w = []
        _w.append(lowui.BigText((_attr, libxyz.const.PROG), _font6x6))
        _w.append(lowui.BigText((_attr, u"Version: %s" %
                                Version.string_version), _font6x6))
        _w.append(lowui.BigText((_attr, u"Homepage: %s" %
                                libxyz.const.HOMEPAGE), _font6x6))
        #_box = lowui.Pile(_w)
        _box = lowui.Filler(lowui.Pile(_w))

        _box = lowui.Overlay(_box, self.xyz.top, uilib.align.CENTER, None,
                             uilib.align.MIDDLE, None)

        _dim = self.xyz.screen.get_cols_rows()
        self.xyz.screen.draw_screen(_dim, _box.render(_dim, True))

        _input = None

        while True:
            _input = self.xyz.input.get()

            if _input:
                break
