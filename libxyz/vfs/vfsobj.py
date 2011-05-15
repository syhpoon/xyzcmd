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

from libxyz.core.utils import bstring, ustring
from libxyz.vfs import types, util

class VFSObject(object):
    """
    Abstract interface for VFS objects
    """

    def __init__(self, xyz, path, full_path, ext_path, driver, parent,
                 enc=None, **kwargs):
        self.xyz = xyz
        self.enc = enc or xyzenc
        # Internal VFS path
        self.path = bstring(path, self.enc)
        # Full VFS path
        self.full_path = bstring(full_path, self.enc)
        # External VFS path
        self.ext_path = bstring(ext_path, self.enc)
        self.parent = parent
        self.driver = driver
        self.kwargs = kwargs
        self.fileobj = None

        # File name
        self.name = os.path.basename(self.path)

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

        self.__ni_msg = _(u"Feature not implemented")

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

    def is_dir_empty(self):
        """
        Return True if instance is representing directory and it is empty
        """

        if not self.is_dir():
            return False

        _, _, objs = self.walk()

        return len(objs) == 0

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

    def copy(self, path, existcb=None, errorcb=None,
             save_attrs=True, follow_links=False, cancel=None):
        """
        Copy file to specified location

        @param path: Local path to copy file to
        @param existcb: Callback function to be called if there exists
                        an object in target directory with the same name.
                        Callback function receives VFSObject instance as an
                        argument and must return one of:
                        'override' - to override this very object
                        'override all' - to override any future collisions
                        'skip' - to skip the object
                        'skip all' - to skip all future collisions
                        'abort' - to abort the process.
                        If no existscb provided 'abort' is used as default
        @param errorcb: Callback function to be called in case an error occured
                        during copying. Function receives VFSObject instance
                        and error string as arguments and must return one of:
                        'skip' - to continue the process
                        'skip all' - to skip all future errors
                        'abort' - to abort the process.
                        If no errorcb provided 'abort' is used as default
        @param save_attrs: Whether to save object attributes
        @param follow_links: Whether to follow symlinks
        @param cancel: a threading.Event instance, if it is found set - abort
        """

        raise NotImplementedError(self.__ni_msg)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def move(self, path, existcb=None, errorcb=None, save_attrs=True,
             follow_links=False, cancel=None):
        """
        Move object
        Arguments are the same as for copy()
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
        Directory tree walker
        """

        raise NotImplementedError(self.__ni_msg)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def open(self, mode='r'):
        """
        Open self object in provided mode
        """

        raise NotImplementedError(self.__ni_msg)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def close(self):
        """
        Close self object
        """

        raise NotImplementedError(self.__ni_msg)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def read(self, bytes=None):
        """
        Read bytes from self object
        """

        raise NotImplementedError(self.__ni_msg)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def tell(self):
        """
        Tell file position
        """

        raise NotImplementedError(self.__ni_msg)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def seek(self, offset, whence=None):
        """
        Perform seek() on object
        """

        raise NotImplementedError(self.__ni_msg)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def in_dir(self, d, e):
        """
        Filter only those archive entries which exist in the same
        directory level
        """

        if e.startswith(d.lstrip(os.sep)) and \
           len(util.split_path(e)) == (len(util.split_path(d)) + 1):
            return True
        else:
            return False

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    def __repr__(self):
        return self.__str__()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __unicode__(self):
        return ustring(self.__str__())

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _prepare(self):
        raise NotImplementedError(self.__ni_msg)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __del__(self):
        if self.fileobj:
            try:
                self.close()
            except Exception:
                pass
