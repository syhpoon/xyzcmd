#-*- coding: utf8 -*
#
# Max E. Kuznecov 2008
#

from libxyz.core.plugins import BasePlugin
from libxyz.core.utils import ustring

from libxyz.ui import lowui
from libxyz.ui import XYZListBox

class XYZPlugin(BasePlugin):
    "Plugin fileinfo"

    NAME = u"fileinfo"
    AUTHOR = u"Max E. Kuznecov"
    VERSION = u"0.1"
    BRIEF_DESCRIPTION = _(u"Show VFS object information")
    FULL_DESCRIPTION = _(u"Show detailed information provided by VFS layer")
    NAMESPACE = u"vfs"
    MIN_XYZ_VERSION = None
    DOC = None
    HOMEPAGE = u"xyzcmd.syhpoon.name"
    EVENTS = [(u"fileinfo",
               _(u"Event is fired upon showing file-info dialog.\n"\
                 u"Arguments: Currently selected VFSObject instance")),
              ]

    def __init__(self, xyz):
        super(XYZPlugin, self).__init__(xyz)

        self.export(self.fileinfo)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def fileinfo(self):
        """
        Show VFS object info
        """

        _selected = self.xyz.pm.from_load(":sys:panel", "get_selected")()
        self.fire_event("fileinfo", _selected)

        _data = []
        _na = lambda x: lowui.Text(u"%-30s: N/A" % x)

        for _name, _value in _selected.attributes:
            if _value in (None, ""):
                _data.append(_na(_name))
            else:
                if not isinstance(_value, basestring):
                    _value = ustring(str(_value))

                _data.append(lowui.Text(u"%-30s: %s" % (_name, _value)))

        _walker = lowui.SimpleListWalker(_data)
        _dim = tuple([x - 2 for x in self.xyz.screen.get_cols_rows()])

        XYZListBox(self.xyz, self.xyz.top, _walker, _(u"VFS Object Info"),
                   _dim).show()
