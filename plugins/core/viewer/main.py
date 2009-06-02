#-*- coding: utf8 -*
#
# Max E. Kuznecov <syhpoon@syhpoon.name> 2008
#

import libxyz
import libxyz.ui as uilib

from libxyz.core.plugins import BasePlugin
from libxyz.ui import lowui
from libxyz.exceptions import XYZError
from libxyz.exceptions import PluginError

import filewalker

class XYZPlugin(BasePlugin):
    "Plugin viewer"

    NAME = u"viewer"
    AUTHOR = u"Max E. Kuznecov <syhpoon@syhpoon.name>"
    VERSION = u"0.1"
    BRIEF_DESCRIPTION = u"File viewer"
    FULL_DESCRIPTION = u""
    NAMESPACE = u"core"
    MIN_XYZ_VERSION = None
    DOC = None
    HOMEPAGE = "xyzcmd.syhpoon.name"

    def __init__(self, xyz):
        super(XYZPlugin, self).__init__(xyz)

        self.export(self.view)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def view(self, filename):
        """
        View file
        """

        try:
            _walker = filewalker.FileWalker(filename)
        except XYZError, e:
            raise PluginError(e.message)

        _attr = lambda x: self.xyz.skin.get_palette(u"plugin.viewer", x)
        _dim = self.xyz.screen.get_cols_rows()

        _header = lowui.AttrWrap(lowui.Text("[FILE] 100b,20L 0%"),
                                 _attr("statusbar"))

        _lbox = lowui.ListBox(_walker)
        _frame = lowui.Frame(lowui.AttrWrap(_lbox, _attr("window")),
                                            header=_header)

        while True:
            _canvas = _frame.render(_dim, focus=0)

            self.xyz.screen.draw_screen(_dim, _canvas)

            try:
                _raw = self.xyz.input.get()

                if self.xyz.input.WIN_RESIZE in _raw:
                    _dim = self.xyz.screen.get_cols_rows()
                    continue
                    
                if self._keys.ESCAPE in _raw or self._keys.ENTER in _raw:
                    break
            except Exception:
                break
