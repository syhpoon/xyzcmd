#-*- coding: utf8 -*
#
# Max E. Kuznecov <syhpoon@syhpoon.name> 2008
#

from libxyz.core.plugins import BasePlugin

from libxyz.ui import lowui

import libxyz.ui as uilib

class XYZPlugin(BasePlugin):
    """
    Plugin testinput
    """

    NAME = u"testinput"
    AUTHOR = u"Max E. Kuznecov <syhpoon@syhpoon.name>"
    VERSION = u"0.1"
    BRIEF_DESCRIPTION = u"Test input"
    FULL_DESCRIPTION = u""
    NAMESPACE = u"ui"
    MIN_XYZ_VERSION = None
    DOC = None
    HOMEPAGE = u"xyzcmd.syhpoon.name"

    def __init__(self, xyz):
        super(XYZPlugin, self).__init__(xyz)

        self.public = {u"show_box": self._show_box}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _show_box(self):
        """
        Show test_box dialog
        """

        _msg = _(u"Press any key. Escape twice to quit.")

        _escape = 0

        while True:
            _input = uilib.MessageBox(self.xyz, self.xyz.top, _msg,
                                     _(u"Input test")).show()

            if uilib.Keys.ESCAPE in _input:
                _escape += 1
                if _escape == 2:
                    return
            else:
                _escape = 0

            _msg = unicode(_input)
