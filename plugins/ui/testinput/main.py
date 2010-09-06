#-*- coding: utf8 -*
#
# Max E. Kuznecov <syhpoon@syhpoon.name> 2008
#

from libxyz.core.plugins import BasePlugin
from libxyz.core.utils import ustring, bstring

import libxyz.ui as uilib

class XYZPlugin(BasePlugin):
    """
    Plugin testinput
    """

    NAME = u"testinput"
    AUTHOR = u"Max E. Kuznecov <syhpoon@syhpoon.name>"
    VERSION = u"0.2"
    BRIEF_DESCRIPTION = _(u"Test input")
    FULL_DESCRIPTION = _(u"Simple dialog to show pressed keys.\n"\
                         u"Shortcut is what XYZCommander expects to see in "\
                         u"configuration files.\n"\
                         u"Raw is what low-level library emits to focus "\
                         u"widget.\n"\
                         u"If any keybinding currently exists for key it is "\
                         u"shown on the bottom line"
                         )
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
        _escape_key = uilib.Shortcut(sc=[self._keys.ESCAPE])

        while True:
            shortcut = InputBox(self.xyz, self.xyz.top, bstring(_msg),
                                _(u"Input test")).show(use_wrap=use_wrap)

            if shortcut == _escape_key:
                _escape += 1
                if _escape == 2:
                    return
            else:
                _escape = 0

            method = self.xyz.km.get_method_by_key(shortcut)

            _msg = u"Shortcut: '%s'. Raw: '%s'" % (
                   (u" ".join([ustring(x) for x in shortcut.sc]),
                    u" ".join([ustring(x) for x in shortcut.raw])))

            if method is not None:
                _msg = u"%s\n[%s]" % (_msg, method.ns)

#++++++++++++++++++++++++++++++++++++++++++++++++

class InputBox(uilib.MessageBox):
    def show(self, dim=None, use_wrap=True):
        def _get_input():
            if use_wrap:
                return self.xyz.input.get()
            else:
                return self.screen.get_input()

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        if dim is None:
            dim = self.screen.get_cols_rows()

        self.screen.draw_screen(dim, self.render(dim, True))

        _input = None

        while True:
            _input = _get_input()

            if self.xyz.km.is_prefix(uilib.Shortcut(raw=_input)):
                _input += _get_input()

            if _input:
                break

        return uilib.Shortcut(raw=_input)
