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

import re
import os

from libxyz.vfs import VFSObject
from libxyz.exceptions import VFSError

class VFSDispatcher(object):
    TAG = "#vfs#"
    
    def __init__(self, xyz):
        self.xyz = xyz
        self._handlers = {}
        self.matchre = re.compile(r"^(?:(\w+):)?(.+?)(?:(%s){1}(.*))?\s*$" %
                                  self.TAG)

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

    def dispatch(self, path, enc=None):
        """
        Dispatch provided path to corresponding VFS object handler
        """

        enc = enc or xyzenc
        
        result = self.matchre.search(path)

        if result is None:
            raise VFSError(_(u"Invalid path: %s.") % path )
        
        prefix, ext_path, tag, int_path = result.groups()

        if prefix and not tag and int_path is None:
            int_path = ""
            path += self.TAG

        if prefix not in self._handlers:
            raise VFSError(_(u"Unable to find VFS handler for prefix %s.") %
                           prefix)
        else:
            return self._handlers[prefix](self.xyz, path, ext_path,
                                          int_path, enc)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_file_by_path(self, path):
        f = os.path.split(path)
        obj = self.dispatch(path)
        xyzlog.info(f)
        xyzlog.error(obj.full_path)
        
