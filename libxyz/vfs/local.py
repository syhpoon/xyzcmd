#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <syhpoon@syhpoon.name> 2008
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

import os
import os.path
import stat

from libxyz.exceptions import VFSError
from libxyz.exceptions import XYZRuntimeError
from libxyz.vfs import vfsobj
from libxyz.vfs import types
from libxyz.vfs import util
from libxyz.vfs import mode

class LocalVFSObject(vfsobj.VFSObject):
    """
    Local VFS object is used to access local filesystem
    """

    def walk(self, top=None):
        """
        Directory tree walker
        @param top: Top directory or self.path unless provided
        @return: tuple (parent, dir, dirs, files) where:
                 parent - parent dir LocalVFSFile instance
                 dir - current dir LocalVFSFile instance
                 dirs - list of LocalVFSFile objects of directories
                 files - list of LocalVFSFile objects of files
        """

        top = top or self.path

        try:
            _dir, _dirs, _files = os.walk(top).next()
        except StopIteration:
            raise XYZRuntimeError(_(u"Unable to walk on %s") % top)

        _abstop = os.path.abspath(top)

        _dirs.sort()
        _files.sort()

        _parent = LocalVFSFile(os.path.dirname(_dir), self.enc)
        _parent.name = u".."

        if not isinstance(_parent.ftype, types.VFSTypeLink):
            _parent.visual = u"/.."

        return [
                _parent,
                LocalVFSFile(_dir, self.enc),
                [LocalVFSFile(os.path.join(_abstop, x), self.enc)
                 for x in _dirs],
                [LocalVFSFile(os.path.join(_abstop, x), self.enc)
                 for x in _files],
               ]

#++++++++++++++++++++++++++++++++++++++++++++++++

class LocalVFSFile(vfsobj.VFSFile):
    """
    Local file object
    """

    def __init__(self, path, enc):
        super(LocalVFSFile, self).__init__(path, enc)

        self.ftype = self._find_type(path)
        self.vtype = self.ftype.vtype

        self._set_attributes()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return "<LocalVFSFile object: %s>" % os.path.join(self.path, self.name)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __repr__(self):
        return self.__str__()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _find_type(self, path):
        """
        Find out file type
        """

        try:
            self._stat = os.lstat(path)
        except OSError, e:
            raise VFSError(_(u"Unable to stat file %s: %s" % (path, str(e))))

        return util.get_file_type(self._stat.st_mode)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _set_attributes(self):
        """
        Set file attibutes
        """

        def set_link_attributes():
            """
            Set appropriate soft link attibutes
            """

            _realpath = os.readlink(self.path)
            _fullpath = os.path.realpath(self.path)

            if not os.path.exists(_fullpath):
                self.vtype = u"!"
            else:
                try:
                    self.data = LocalVFSFile(_fullpath, self.enc)
                except VFSError, e:
                    xyzlog.log(_("Error creating VFS object: %s") % str(e),
                              xyzlog.loglevel.ERROR)
                else:
                    if isinstance(self.data.ftype, types.VFSTypeDir):
                        self.vtype = u"~"

            self.info = u""
            self.visual = u"-> %s" % _realpath.decode(self.enc)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def set_char_attributes():
            """
            Set appropriate character device attibutes
            """

            _dev = self._stat.st_rdev
            self.info = u"%s, %s %s" % (os.major(_dev), os.minor(_dev),
                                        self.mode)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.atime = self._stat.st_atime
        self.mtime = self._stat.st_mtime
        self.ctime = self._stat.st_ctime
        self.size = self._stat.st_size
        self.uid = self._stat.st_uid
        self.gid = self._stat.st_gid
        self.mode = mode.Mode(self._stat.st_mode)
        self.visual = u"%s%s" % (self.vtype, self.name)
        self.info = u"%s %s" % (self.size, self.mode)

        if isinstance(self.ftype, types.VFSTypeLink):
            set_link_attributes()
        elif isinstance(self.ftype, types.VFSTypeChar):
            set_char_attributes()
        elif isinstance(self.ftype, types.VFSTypeFile):
            _mode = stat.S_IMODE(self.mode.raw)

            # Executable
            if _mode & 0111:
                self.vtype = u"*"
                self.visual = u"*%s" % self.name
