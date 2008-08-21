#-*- coding: utf8 -*
#
# Max E. Kuznecov <syhpoon@syhpoon.name> 2008
#

from libxyz.core.plugins import BasePlugin
from libxyz.ui import lowui

import libxyz.ui as uilib

class XYZPlugin(BasePlugin):
    "Plugin bindlist"

    NAME = u"bindlist"
    AUTHOR = u"Max E. Kuznecov <syhpoon@syhpoon.name>"
    VERSION = u"0.1"
    BRIEF_DESCRIPTION = u"Show keybindings"
    FULL_DESCRIPTION = u"Plugin is used to display all current keybindings "\
                       u"along with corresponding contextes and methods"
    NAMESPACE = u"core"
    HOMEPAGE = u"xyzcmd.syhpoon.name"

    def __init__(self, xyz):
        super(XYZPlugin, self).__init__(xyz)

        self.export(self.show_binds)

        self._keys = uilib.Keys()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def show_binds(self):
        """
        Show keybindings
        """

        _data = self.xyz.km.get_binds()

        _entries = []

        _divattr = self.xyz.skin.attr(uilib.XYZListBox.resolution, u"border")

        _entries.append(lowui.Text(u"%-15s %-15s %s" %
                        (_(u"Context"), _(u"Bind"), _(u"Method"))))
        _entries.append(uilib.Separator(div_attr=_divattr))

        for _context in sorted(_data.keys()):
            for _bind in sorted(_data[_context].keys()):
                if _data[_context][_bind] is None:
                    continue

                _entries.append(lowui.Text(u"%-15s %-15s %s" %
                                (_context,
                                 self._keys.raw_to_shortcut(_bind[0]),
                                 _data[_context][_bind].ns)))

        _walker = lowui.SimpleListWalker(_entries)

        _dim = tuple([x - 2 for x in self.xyz.screen.get_cols_rows()])

        uilib.XYZListBox(self.xyz, self.xyz.top, _walker,
                         _(u"Keybindings"), _dim).show()
