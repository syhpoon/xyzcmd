#-*- coding: utf8 -*
#
# Max E. Kuznecov <syhpoon@syhpoon.name> 2008
#

from libxyz.core.plugins import BasePlugin
from libxyz.ui import lowui
from libxyz.core.utils import ustring, bstring

import libxyz.ui as uilib

class XYZPlugin(BasePlugin):
    """
    Plugin testinput
    """

    NAME = u"testinput"
    AUTHOR = u"Max E. Kuznecov <syhpoon@syhpoon.name>"
    VERSION = u"0.1"
    BRIEF_DESCRIPTION = u"Test input"
    FULL_DESCRIPTION = u"Simple dialog to show pressed keys.\n"\
                       u"Shortcut is what XYZCommander expects to see in "\
                       u"configuration files.\n"\
                       u"Raw is what low-level library emits to focus widget"
    NAMESPACE = u"ui"
    MIN_XYZ_VERSION = None
    DOC = None
    HOMEPAGE = u"xyzcmd.syhpoon.name"

    def __init__(self, xyz):
        super(XYZPlugin, self).__init__(xyz)

        self.export(self.show_box)

        self._keys = uilib.Keys()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def show_box(self, use_wrap=True):
        """
        Show test_box dialog
        @param use_wrap: Whether to use input wrapper which honours
        learned keys
        """

        _msg = _(u"Press any key. Escape twice to quit.")

        _escape = 0

        while True:
            _input = InputBox(self.xyz, self.xyz.top, bstring(_msg),
                              _(u"Input test")).show(use_wrap=use_wrap)

            if self._keys.ESCAPE in _input:
                _escape += 1
                if _escape == 2:
                    return
            else:
                _escape = 0

            _keys = []

            for _i in _input:
                _keys.append(self._keys.raw_to_shortcut(ustring(_i)))

            _low = [ustring(x) for x in _input]
            _msg = u"Shortcut: '%s'. Raw: '%s'" % \
                   (u"".join(_keys), u"".join(_low))

#++++++++++++++++++++++++++++++++++++++++++++++++

class InputBox(uilib.MessageBox):
    def show(self, dim=None, use_wrap=True):
        if dim is None:
            dim = self.screen.get_cols_rows()

        self.screen.draw_screen(dim, self.render(dim, True))

        _input = None

        while True:
            if use_wrap:
                _input = self.xyz.input.get()
            else:
                _input = self.screen.get_input()

            if _input:
                break

        return _input
