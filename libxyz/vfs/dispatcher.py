#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008-2009
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

"""
VFSDispatcher - Dispatching to appropriate VFS module based on path.
Path format is following:
[<prefix>]:<path_to_archive>#vfs#<path_inside_archive>
"""

import os
import re

from libxyz.vfs import VFSObject
from libxyz.exceptions import VFSError

class VFSDispatcher(object):
    def __init__(self, xyz):
        self.xyz = xyz
        self._handlers = {}
        self.vfsre = re.compile(r'(#vfs-\w+#)')
        self.vfsre2 = re.compile(r'^#vfs-(\w+)#$')

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def register(self, prefix, vfs_obj_class):
        """
        Register new VFS handler

        @param prefix: Patch prefix
        @param vfs_obj_class: VFSObject derived class
        """

        if not issubclass(vfs_obj_class, VFSObject):
            raise VFSError(
                _(u"Invalid class: %s. VFSObject dervied expected.") %
                str(vfs_obj_class))

        self._handlers[prefix] = vfs_obj_class

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def dispatch(self, path, enc=None, **kwargs):
        """
        Dispatch provided path to corresponding VFS object handler
        """

        enc = enc or xyzenc

        data = self._parse_path(path)

        if not data:
            raise VFSError(_(u"Invalid path: %s.") % path)

        handler = None

        for p, vfs in data:
            if vfs not in self._handlers:
                raise VFSError(
                    _(u"Unable to find VFS handler for %s.") % vfs)
            else:
                full_path = self.get_full_path(p, vfs, handler)
                ext_path = self.get_ext_path(handler, vfs)

                handler = self._handlers[vfs](
                    self.xyz,
                    os.path.abspath(os.path.normpath(p)),
                    full_path,
                    ext_path,
                    vfs,
                    handler,
                    enc,
                    **kwargs)

        return handler

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _parse_path(self, path):
        files = []

        driver = None

        for entry in re.split(self.vfsre, path):
            entry = os.sep if not entry else entry
            
            vfs = self.vfsre2.search(entry)

            if driver is not None:
                files.append((entry, driver))
                driver = None
            elif vfs:
                driver = vfs.group(1)
            else:
                files.append((entry, None))

        return files

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_parent(self, path, enc):
        _parent = self.xyz.vfs.dispatch(
            os.path.abspath(os.path.dirname(path)), enc)
        _parent.name = ".."

        return _parent

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_full_path(self, path, vfs, parent):
        """
        Return full path
        """
        
        return (parent.full_path if parent else "") + \
               ("#vfs-%s#" % vfs if vfs else "") + path

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_ext_path(self, parent, vfs):
        """
        Return external path
        """
        
        return (parent.full_path if parent else "") + \
               ("#vfs-%s#" % vfs if vfs else "")
