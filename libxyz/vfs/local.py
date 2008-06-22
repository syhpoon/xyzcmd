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
from libxyz.vfs import vfsobj
from libxyz.vfs import types
from libxyz.vfs import util
from libxyz.vfs import mode

class LocalVFSObject(vfsobj.VFSObject):
    """
    Local VFS object is used to access local filesystem
    """

    def __init__(self, path):
        super(LocalVFSObject, self).__init__(path)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def walk(self, top=None):
        """
        Directory tree generator
        @param top: Top directory or self.path unless provided
        @return: tuple (dir, dirs, files) where:
                 dir - current dir name
                 dirs - list of LocalVFSFile objects of directories
                 files - list of LocalVFSFile objects of files
        """

        top = top or self.path
        _dir, _dirs, _files = os.walk(top).next()
        _abstop = os.path.abspath(top)

        return [
                _dir,
                [LocalVFSFile(os.path.join(_abstop, x)) for x in _dirs],
                [LocalVFSFile(os.path.join(_abstop, x)) for x in _files],
               ]

#++++++++++++++++++++++++++++++++++++++++++++++++

class LocalVFSFile(vfsobj.VFSFile):
    """
    Local file object
    """

    def __init__(self, path):
        super(LocalVFSFile, self).__init__(path)

        self.ftype = self._find_type(path)
        self.visual = self.ftype.visual

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

        self.atime = self._stat.st_atime
        self.mtime = self._stat.st_mtime
        self.ctime = self._stat.st_ctime
        self.size = self._stat.st_size
        self.uid = self._stat.st_uid
        self.gid = self._stat.st_gid
        self.mode = mode.Mode(self._stat.st_mode)
