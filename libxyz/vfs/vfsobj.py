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

VFS_NONE = None

class VFSObject(object):
    """
    Abstract interface for VFS objects
    """

    def __init__(self, path):
        self.path = path

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def open(self):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def close(self):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def read(self):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def write(self):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def flush(self):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def walk(self):
        """
        Directory tree generator
        """

        pass

#++++++++++++++++++++++++++++++++++++++++++++++++

def VFSFile(object):
    """
    A VFS file information
    """

    def __init__(self):
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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def VFSDir(VFSFile):
    """
    A VFS directory information
    """

    pass
