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
import time
import pwd
import grp

from libxyz.exceptions import VFSError
from libxyz.exceptions import XYZRuntimeError
from libxyz.exceptions import XYZValueError
from libxyz.vfs import vfsobj
from libxyz.vfs import types
from libxyz.vfs import util
from libxyz.vfs import mode
from libxyz.core.utils import ustring

class LocalVFSObject(vfsobj.VFSObject):
    """
    Local VFS object is used to access local filesystem
    """

    def _prepare(self):
        self.ftype = self._find_type(self.path)
        self.vtype = self.ftype.vtype

        self._set_attributes()

        _time = lambda x: ustring(time.ctime(x))
                
        self.attributes = (
            (_(u"Name"), self.name),
            (_(u"Type"), self.ftype),
            (_(u"Access time"), _time(self.atime)),
            (_(u"Modification time"), _time(self.mtime)),
            (_(u"Change time"), _time(self.ctime)),
            (_(u"Size in bytes"), ustring(self.size)),
            (_(u"Owner"), self._uid(self.uid)),
            (_(u"Group"), self._gid(self.gid)),
            (_(u"Access mode"), ustring(self.mode)),
            (_(u"Inode"), ustring(self.inode)),
            (_(u"Type-specific data"), self.data),
            )

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return "<LocalVFSObject object: %s>" % self.path

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _uid(self, uid):
        try:
            _name = pwd.getpwuid(uid).pw_name
        except (KeyError, TypeError):
            _name = None

        if _name is not None:
            return u"%s (%s)" % (ustring(uid), _name)
        else:
            return ustring(uid)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _gid(self, gid):
        try:
            _name = grp.getgrgid(gid).gr_name
        except (KeyError, TypeError):
            _name = None

        if _name is not None:
            return u"%s (%s)" % (ustring(gid), _name)
        else:
            return ustring(gid)
        
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
                    self.data = self.xyz.vfs.dispatch(_fullpath, self.enc)
                except VFSError, e:
                    xyzlog.error(_(u"Error creating VFS object: %s") %
                                 ustring(str(e)))
                else:
                    if isinstance(self.data.ftype, types.VFSTypeDir):
                        self.vtype = u"~"
            self.info = u""
            self.visual = u"-> %s" % ustring(_realpath, self.enc)

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
        self.inode = self._stat.st_ino
        self.mode = mode.Mode(self._stat.st_mode, self.ftype)
        self.visual = u"%s%s" % (self.vtype, self.name)
        self.info = u"%s %s" % (util.format_size(self.size), self.mode)

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

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def walk(self):
        """
        Directory tree walker
        @return: tuple (parent, dir, dirs, files) where:
                 parent - parent dir LocalVFSObject instance
                 dir - current LocalVFSObject instance
                 dirs - list of LocalVFSObject objects of directories
                 files - list of LocalVFSObject objects of files
        """

        try:
            _dir, _dirs, _files = os.walk(self.path).next()
        except StopIteration:
            raise XYZRuntimeError(_(u"Unable to walk on %s") %
                                  ustring(self.path))

        _dirs.sort()
        _files.sort()
        _parent = self.xyz.vfs.get_parent(_dir, self.enc)

        get_path = lambda x: os.path.abspath(os.path.join(self.path, x))
        
        return [
            _parent,
            self,
            [self.xyz.vfs.dispatch(get_path(x), self.enc) for x in _dirs],
            [self.xyz.vfs.dispatch(get_path(x), self.enc) for x in _files],
            ]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def remove(self):
        """
        Tell object to remove itself
        """

        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def mkdir(self, newdir):
        """
        Create new dir inside object (only valid for directory object types)
        """

        if not isinstance(self.ftype, types.VFSTypeDir):
            raise XYZValueError(
                _(u"Unable to create directory inside %s object type") %
                self.ftype)
        else:
            try:
                os.mkdir(os.path.join(self.path, newdir))
            except Exception, e:
                raise XYZRuntimeError(_(u"Unable to create directory: %s") %
                                      ustring(str(e)))
                        
