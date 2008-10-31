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

class VFSObject(object):
    """
    Abstract interface for VFS objects
    """

    def __init__(self, path, enc=None):
        self.enc = enc or xyzenc

        if isinstance(path, unicode):
            self.path = path.encode(self.enc)
        else:
            self.path = path

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def walk(self):
        """
        Directory tree generator
        """

        return None

#++++++++++++++++++++++++++++++++++++++++++++++++

class VFSFile(object):
    """
    A VFS file information interface
    """

    def __init__(self, path, enc=None):
        self.path = os.path.abspath(path)
        self.enc = enc or "utf8"

        # File name
        self.name = os.path.basename(self.path).decode(self.enc)

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
