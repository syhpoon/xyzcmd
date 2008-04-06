#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
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

import libxyz.vfs as vfs

from libxyz.exceptions import VFSError
from libxyz.vfs import types
from libxyz.vfs import util
from libxyz.vfs import mode

class LocalVFSObject(vfs.VFSObject):
    """
    Local VFS object is used to access local filesystem
    """

    def __init__(self, path):
        super(LocalVFSObject, self).__init__(path)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def list(self, directory):
        """
        Directory iterator
        """

        for _entry in os.listdir(directory):
            yield LocalVFSFile(os.path.join(os.path.absfile(directory), _entry)

#++++++++++++++++++++++++++++++++++++++++++++++++

class LocalVFSFile(vfs.VFSFile):
    """
    Local file object
    """

    def __init__(self, path):
        self.name = os.path.basename(path)
        self.ftype = self._find_type(path)

        self._set_attributes(self.ftype)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _find_type(self, path):
        """
        Find out file type
        """

        try:
            self._stat = os.stat(path)
        except OSError, e:
            raise VFSError(_(u"Unable to stat file %s: %s" % (path, str(e))))

        return vfsutil.get_file_type(self._stat.st_mode)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _set_attributes(self, ftype):
        """
        Set object attributes
        """

        self._set_attributes()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _set_attributes(self, path):
        """
        Set file attibutes
        """

        self.atime = self._stat.st_atime
        self.mtime = self._stat.st_mtime
        self.ctime = self._stat.st_ctime
        self.size = self._stat.st_size
        self.uid = self._stat.st_uid
        self.gid = self._stat.st_gid
        self.mode = vfsmode.VFSMode(self._stat.st_mode, filetype=self.ftype)
