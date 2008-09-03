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

import os.path

VFS_NONE = None

class VFSObject(object):
    """
    Abstract interface for VFS objects
    """

    def __init__(self, path, enc=None):
        self.path = path
        self.enc = enc or "utf8"

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def walk(self):
        """
        Directory tree generator
        """

        return VFS_NONE

#++++++++++++++++++++++++++++++++++++++++++++++++

class VFSFile(object):
    """
    A VFS file information interface
    """

    def __init__(self, path, enc=None):
        self.path = os.path.abspath(path)
        self.enc = enc or "utf8"

        # File name
        self.name = os.path.basename(self.path)

        # File type
        self.ftype = VFS_NONE

        # Access time
        self.atime = VFS_NONE

        # Modified time
        self.mtime = VFS_NONE

        # Changed time
        self.ctime = VFS_NONE

        # Size in bytes
        self.size = VFS_NONE

        # Owner UID
        self.uid = VFS_NONE

        # Group
        self.gid = VFS_NONE

        # Mode
        self.mode = VFS_NONE

        # Visual file type
        self.vtype = VFS_NONE

        # Visual file representation
        self.visual = VFS_NONE

        # File info
        self.info = VFS_NONE

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def open(self):
        return VFS_NONE

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def close(self):
        return VFS_NONE

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def read(self):
        return VFS_NONE

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def write(self):
        return VFS_NONE

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def flush(self):
        return VFS_NONE
