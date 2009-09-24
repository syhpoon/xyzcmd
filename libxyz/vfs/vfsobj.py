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

from libxyz.core import utils
from libxyz.vfs import types

class VFSObject(object):
    """
    Abstract interface for VFS objects
    """

    def __init__(self, xyz, path, full_path, ext_path, driver, parent,
                 enc=None, **kwargs):
        self.xyz = xyz
        self.enc = enc or xyzenc
        self.path = path
        self.full_path = full_path
        self.ext_path = ext_path
        self.parent = parent
        self.driver = driver
        self.kwargs = kwargs

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

        # Run local constructor
        self._prepare()

        __ni_msg = _(u"Feature not implemented")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def is_file(self):
        """
        Return True if instance is representing regular file
        """
        
        return isinstance(self.ftype, types.VFSTypeFile)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def is_dir(self):
        """
        Return True if instance is representing directory
        """

        return isinstance(self.ftype, types.VFSTypeDir)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def is_link(self):
        """
        Return True if instance is representing soft link
        """

        return isinstance(self.ftype, types.VFSTypeLink)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def is_char(self):
        """
        Return True if instance is representing soft char device
        """

        return isinstance(self.ftype, types.VFSTypeChar)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def is_block(self):
        """
        Return True if instance is representing block device
        """

        return isinstance(self.ftype, types.VFSTypeBlock)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def is_fifo(self):
        """
        Return True if instance is representing FIFO
        """

        return isinstance(self.ftype, types.VFSTypeFifo)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def is_socket(self):
        """
        Return True if instance is representing socket
        """

        return isinstance(self.ftype, types.VFSTypeSocket)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def copy(self, path):
        """
        Copy file to specified location
        """

        raise NotImplementedError(self.__ni_msg)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def mkdir(self, newdir):
        """
        Create new dir inside object (only valid for directory object types)
        """

        raise NotImplementedError(self.__ni_msg)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def remove(self, recursive=True):
        """
        [Recursively] remove object
        """

        raise NotImplementedError(self.__ni_msg)
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def walk(self):
        """
        Directory tree generator
        """

        raise NotImplementedError(self.__ni_msg)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __repr__(self):
        return self.__str__()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def _prepare(self):
        raise NotImplementedError(self.__ni_msg)

