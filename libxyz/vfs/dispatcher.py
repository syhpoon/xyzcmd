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
<path_to_archive>#vfs-<driver>#<path_inside_vfs>
"""

import os
import re
import time

from libxyz.vfs import VFSObject
from libxyz.exceptions import VFSError

class VFSDispatcher(object):
    def __init__(self, xyz):
        self.xyz = xyz
        self._handlers = {}
        self._cache = {}
        self._cache_data = {}

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
                _(u"Invalid class: %s. VFSObject derived expected.") %
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

    def set_cache(self, path, data):
        """
        Save some data for VFS object
        This data dict is appended to VFSObject's kwargs dict
        every time dispatch() is called
        """

        self._cache[path] = data

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_cache(self, path):
        """
        Return saved cache for the object or {} if none was saved
        """

        atime = self._cache_data.get(path, None)
        now = int(time.time())

        # Cache obsoleted
        if atime is not None and \
               now - atime >= self.xyz.conf["vfs"]["cache_time"]:

            self.clear_cache(path)
            del(self._cache_data[path])

            data = None
        else:
            data = self._cache.get(path, None)

        # Update access timestamp
        if data:
            self._cache_data[path] = now

        return data

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def clear_cache(self, path):
        """
        Clear cache for given path
        """

        try:
            del(self._cache[path])
        except KeyError:
            pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _parse_path(self, path):
        files = []

        driver = None

        for entry in re.split(self.vfsre, path):
            if not entry:
                entry = os.sep

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

        if parent:
            p = parent.full_path
        else:
            p = ""

        if vfs:
            v = "#vfs-%s#" % vfs
        else:
            v = ""

        return p + v + path

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_ext_path(self, parent, vfs):
        """
        Return external path
        """

        if parent:
            p = parent.full_path
        else:
            p = ""

        if vfs:
            v = "#vfs-%s#" % vfs
        else:
            v = ""

        return p + v
