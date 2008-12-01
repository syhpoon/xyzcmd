#-*- coding: utf8 -*
#
# Max E. Kuznecov 2008
#

import time
import pwd
import grp

from libxyz.core.plugins import BasePlugin

from libxyz.ui import lowui
from libxyz.ui import XYZListBox

class XYZPlugin(BasePlugin):
    "Plugin fileinfo"

    NAME = u"fileinfo"
    AUTHOR = u"Max E. Kuznecov"
    VERSION = u"0.1"
    BRIEF_DESCRIPTION = u"Show VFS object information"
    FULL_DESCRIPTION = u""
    NAMESPACE = u"vfs"
    MIN_XYZ_VERSION = None
    DOC = None
    HOMEPAGE = None

    def __init__(self, xyz):
        super(XYZPlugin, self).__init__(xyz)

        self.export(self.fileinfo)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def fileinfo(self):
        """
        Show VFS object info
        """

        def _uid(uid):
            try:
                _name = pwd.getpwuid(uid).pw_name
            except (KeyError, TypeError):
                _name = None

            if _name is not None:
                return u"%s (%s)" % (unicode(uid), _name)
            else:
                return unicode(uid)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def _gid(gid):
            try:
                _name = grp.getgrgid(gid).gr_name
            except (KeyError, TypeError):
                _name = None

            if _name is not None:
                return u"%s (%s)" % (unicode(gid), _name)
            else:
                return unicode(gid)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        _time = lambda x: time.ctime(x).decode(xyzenc)

        _attrs = (
            ("name", _(u"Name"), lambda x: x),
            ("ftype", _(u"Type"), lambda x: x),
            ("atime", _(u"Access time"), lambda x: _time(x)),
            ("mtime", _(u"Modification time"), lambda x: _time(x)),
            ("ctime", _(u"Change time"), lambda x: _time(x)),
            ("size", _(u"Size in bytes"), lambda x: unicode(x)),
            ("uid", _(u"Owner's uid"), lambda x: _uid(x)),
            ("gid", _(u"Owner's gid"), lambda x: _gid(x)),
            ("mode", _(u"Access mode"), lambda x: unicode(x)),
            ("inode", _(u"Inode"), lambda x: unicode(x)),
            ("data", _(u"Type-specific data"), lambda x: x),
            )

        _selected = self.xyz.pm.from_load(":sys:panel", "get_selected")()

        _data = []
        _na = lambda x: lowui.Text(u"%-30s: N/A" % x)

        for _attr, _name, _trans in _attrs:
            _value = getattr(_selected, _attr, None)

            if _value is None:
                _data.append(_na(_name))
            else:
                _data.append(lowui.Text(u"%-30s: %s" % (_name,
                                                        _trans(_value))))

        _walker = lowui.SimpleListWalker(_data)
        _dim = tuple([x - 2 for x in self.xyz.screen.get_cols_rows()])

        XYZListBox(self.xyz, self.xyz.top, _walker, _(u"VFS Object Info"),
                   _dim).show()
