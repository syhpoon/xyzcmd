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

from libxyz.core import utils

import os.path

class VFSObject(object):
    """
    Abstract interface for VFS objects
    """

    def __init__(self, xyz, full_path, ext_path, int_path, enc=None):
        self.xyz = xyz
        self.name = os.path.basename(utils.ustring(ext_path))
        self.enc = enc
        self.full_path = full_path
        self.path = utils.bstring(ext_path, enc)
        self.int_path = int_path

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def walk(self):
        """
        Directory tree generator
        """

        raise NotImplementedError()

#++++++++++++++++++++++++++++++++++++++++++++++++

class VFSFile(object):
    """
    A VFS file information interface
    """

    def __init__(self, path, enc=None, obj=None):
        self.enc = enc or xyzenc
        self.obj = obj
        self.path = path
        # File name
        self.name = os.path.basename(utils.ustring(self.path, self.enc))

        # File type
        self.ftype = None

        # Access time
        self.atime = None

        # Modified time
        self.mtime = None

        # Changed time
        self.ctime = None

        # Size in bytes
        self.size = None

        # Owner UID
        self.uid = None

        # Group
        self.gid = None

        # Mode
        self.mode = None

        # Inode
        self.inode = None

        # Visual file type
        self.vtype = None

        # Visual file representation
        self.visual = None

        # File info
        self.info = None

        # Any type-specific data
        self.data = None

        # List of significant attributes
        self.attributes = ()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def open(self):
        return None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def close(self):
        return None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def read(self):
        return None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def write(self):
        return None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def flush(self):
        return None
