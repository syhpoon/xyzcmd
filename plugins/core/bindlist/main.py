#-*- coding: utf8 -*
#
# Max E. Kuznecov <syhpoon@syhpoon.name> 2008
#

from libxyz.core.plugins import BasePlugin
from libxyz.core.utils import bstring
from libxyz.ui import lowui

import libxyz.ui as uilib

class XYZPlugin(BasePlugin):
    "Plugin bindlist"

    NAME = u"bindlist"
    AUTHOR = u"Max E. Kuznecov <syhpoon@syhpoon.name>"
    VERSION = u"0.2"
    BRIEF_DESCRIPTION = _(u"Show keybindings")
    FULL_DESCRIPTION = _(u"Plugin is used to display all current keybindings "\
                         u"along with corresponding contextes and methods")
    NAMESPACE = u"core"
    HOMEPAGE = u"xyzcmd.syhpoon.name"
    EVENTS = [("show_binds",
               _(u"Event is fired before showing dialog. "\
                 u"Receives no arguments.")),
              ]

    def __init__(self, xyz):
        super(XYZPlugin, self).__init__(xyz)

        self.export(self.show_binds)

        self._keys = uilib.Keys()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def show_binds(self):
        """
        Show keybindings
        """

        self.fire_event("show_binds")
        
        _data = self.xyz.km.get_binds()

        _entries = []

        _divattr = self.xyz.skin.attr(uilib.XYZListBox.resolution, u"border")

        _entries.append(lowui.Text(u"%-10s %-20s %s" %
                        (_(u"Context"), _(u"Bind"),
                         _(u"Method / Description"))))
        _entries.append(uilib.Separator(div_attr=_divattr))

        for _context in sorted(_data.keys()):
            for _bind in sorted(_data[_context].keys(),
                                cmp=lambda x, y: cmp(bstring(x), bstring(y))):
                if _data[_context][_bind] is None:
                    continue

                _entries.append(lowui.Text(u"%-10s %-20s %s" %
                                (_context, _bind, _data[_context][_bind].ns)))

        _walker = lowui.SimpleListWalker(_entries)

        _dim = tuple([x - 2 for x in self.xyz.screen.get_cols_rows()])

        uilib.XYZListBox(self.xyz, self.xyz.top, _walker,
                         _(u"Keybindings"), _dim).show()
