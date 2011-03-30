#-*- coding: utf8 -*
#
# Max E. Kuznecov <syhpoon@syhpoon.name> 2008
#
# This file is part of XYZCommander.
# XYZCommander is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# XYZCommander is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser Public License for more details.
# You should have received a copy of the GNU Lesser Public License
# along with XYZCommander. If not, see <http://www.gnu.org/licenses/>.

from libxyz.ui import lowui
from libxyz.ui import Keys
from libxyz.ui import XYZListBox
from libxyz.ui import NumEntry

from libxyz.core.plugins import BasePlugin
from libxyz.core import UserData
from libxyz.core.utils import ustring, bstring
from libxyz.parser import FlatParser
from libxyz.parser import ParsedData

from libxyz.exceptions import XYZRuntimeError
from libxyz.exceptions import ParseError

class XYZPlugin(BasePlugin):
    "Bookmarks - frequently used directories list"

    NAME = u"bookmarks"
    AUTHOR = u"Max E. Kuznecov <syhpoon@syhpoon.name>"
    VERSION = u"0.1"
    BRIEF_DESCRIPTION = _(u"Frequently used directories")
    FULL_DESCRIPTION = u""
    NAMESPACE = u"ui"
    MIN_XYZ_VERSION = None
    DOC = None
    HOMEPAGE = u"http://xyzcmd.syhpoon.name/"

    def __init__(self, xyz):
        super(XYZPlugin, self).__init__(xyz)

        self.export(self.add_bookmark)
        self.export(self.del_bookmark)
        self.export(self.show_bookmarks)
        self.export(self.get_path)

        self._bmsubdir = "data"
        self._bmfile = "bookmarks"
        self._ud = UserData()
        self._keys = Keys()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def add_bookmark(self, path, name=None):
        """
        Add new bookmark entry
        If name is not specified, path is used instead
        """

        if name is None:
            name = path

        path = ustring(path)
        name = ustring(name)

        _data = self._load_data()

        if _data is not None:
            _data[name] = path

        return self._save_data(_data)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def del_bookmark(self, name):
        """
        Delete saved bookmark entry by name
        """

        name = ustring(name)

        _data = self._load_data()

        if _data is not None and name in _data:
            del(_data[name])
            return self._save_data(_data)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_path(self, name):
        """
        Get bookmark path by name
        """

        name = ustring(name)

        _data = self._load_data()

        if _data is not None and name in _data:
            return _data[name]

        return None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def show_bookmarks(self):
        """
        Show currently saved bookmarks and chdir to one of them if needed
        """

        def _enter_cb(num):
            if num >= len(_bookmarks):
                return

            _chdir(_bookmarks.index(num))

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def custom_cb(key, focusw):
            _meth = self.xyz.km.process(key, self.ns.pfull)

            if _meth is not None:
                _meth(focusw.msg)
                return False

            return True

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        _bookmarks = self._load_data()

        if _bookmarks is None:
            return

        _chdir = self.xyz.pm.from_load(u":sys:panel", u"chdir")

        _sel_attr = self.xyz.skin.attr(XYZListBox.resolution, u"selected")
        _wdata = []

        i = 0

        for b in _bookmarks:
            _wdata.append(NumEntry(b, _sel_attr, i, enter_cb=_enter_cb))
            i += 1

        _walker = lowui.SimpleListWalker(_wdata)
        _dim = tuple([x - 2 for x in self.xyz.screen.get_cols_rows()])
        _ek = [self._keys.ENTER]

        XYZListBox(self.xyz, self.xyz.top, _walker, _(u"Bookmarks"),
                   _dim).show(exit_keys=_ek, custom=custom_cb)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _load_data(self):
        """
        Load and parse saved bookmarks from file
        """

        try:
            _file = self._ud.openfile(self._bmfile, "r", self._bmsubdir)
        except XYZRuntimeError, e:
            xyzlog.info(_(u"Unable to open bookmarks file: %s") %
                        unicode(e))
            return ParsedData()

        _parser = FlatParser()

        try:
            return _parser.parse(_file)
        except ParseError, e:
            xyzlog.error(_(u"Error parsing bookmarks file: %s") %
                         unicode(e))
        _file.close()

        return None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _save_data(self, data):
        """
        Save data to bookmarks file
        data is a mapping: {name: path}
        """

        try:
            _file = self._ud.openfile(self._bmfile, "w", self._bmsubdir)
        except XYZRuntimeError, e:
            xyzlog.info("Unable to open bookmarks file: %s" % unicode(e))
            return None

        for _name, _path in data.iteritems():
            _file.write('"%s": "%s"\n' %
                        (bstring(_name), bstring(_path)))

        _file.close()

        return True
