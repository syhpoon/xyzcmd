#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <syhpoon@syhpoon.name> 2008-2009
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
import stat
import tarfile
import time

from libxyz.core.utils import ustring, bstring
from libxyz.vfs import types as vfstypes
from libxyz.vfs import vfsobj
from libxyz.vfs import util
from libxyz.vfs import mode

class TarVFSObject(vfsobj.VFSObject):
    """
    Tar archive interface
    """
    
    either = lambda self, a, b: a if self.root else b()
    get_name = lambda self, x: os.path.basename(x.name)
    get_path = lambda self, x: os.path.join(self.ext_path, x.lstrip(os.sep))

    file_type_map = {
        lambda obj: obj.isfile(): vfstypes.VFSTypeFile(),
        lambda obj: obj.isdir(): vfstypes.VFSTypeDir(),
        lambda obj: obj.issym(): vfstypes.VFSTypeLink(),
        lambda obj: obj.ischr(): vfstypes.VFSTypeChar(),
        lambda obj: obj.isblk(): vfstypes.VFSTypeBlock(),
        lambda obj: obj.isfifo(): vfstypes.VFSTypeFifo(),
        }

    def __init__(self, *args, **kwargs):
        self.tarobj = None
        super(TarVFSObject, self).__init__(*args, **kwargs)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def walk(self):
        """
        Directory tree walker
        @return: tuple (parent, dir, dirs, files) where:
        parent - parent dir *VFSObject instance
        dir - current dir TarVFSObject instance
        dirs - list of TarVFSObject objects of directories
        files - list of TarVFSObject objects of files
        """

        tarobj = self._open_archive()
        entries = tarobj.getmembers()

        _dirs = [x for x in entries if x.isdir() and
                 self.in_dir(self.path, x.name)]
        _files = [x for x in entries if not x.isdir() and
                  self.in_dir(self.path, x.name)]

        _dirs.sort(cmp=lambda x, y: cmp(self.get_name(x),
                                        self.get_name(y)))
        _files.sort(cmp=lambda x, y: cmp(self.get_name(x),
                                         self.get_name(y)))

        if self.path == os.sep:
            _parent = self.xyz.vfs.get_parent(self.parent.path, self.enc)
        else:
            _parent = self.xyz.vfs.dispatch(
                self.get_path(os.path.dirname(self.path)), self.enc,
                tarobj=self.tarobj)
            _parent.name = ".."

        return [
            _parent,
            self,
            [self.xyz.vfs.dispatch(self.get_path(x.name),
                                   self.enc, tarobj=self.tarobj)
             for x in _dirs],
            [self.xyz.vfs.dispatch(self.get_path(x.name),
                                   self.enc, tarobj=self.tarobj)
             for x in _files],
            ]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def _prepare(self):
        self.root = True if self.path == os.sep else False
        self.tarobj = self.kwargs["tarobj"] if "tarobj" in self.kwargs else \
                      None
        self.obj = None if self.root else self._init_obj()

        self.ftype = self._find_type()
        self.vtype = self.ftype.vtype

        self._set_attributes()

        self.attributes = (
            (_(u"Name"), ustring(self.name)),
            (_(u"Type"), ustring(self.ftype)),
            (_(u"Modification time"), ustring(time.ctime(self.mtime))),
            (_(u"Size in bytes"), ustring(self.size)),
            (_(u"Owner"), ustring(self.uid)),
            (_(u"Group"), ustring(self.gid)),
            (_(u"Access mode"), ustring(self.mode)),
            (_(u"Type-specific data"), self.data),
            )

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return "<TarVFSObject object: %s>" % self.path

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def in_dir(self, d, e):
        """
        Filter only those archive entries which exist in the same
        directory level
        """

        return True if e.startswith(d.lstrip(os.sep)) and \
               len(util.split_path(e)) == (len(util.split_path(d)) + 1) \
               else False

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def _find_type(self):
        """
        Find out file type
        """

        if self.root:
            return self.parent.ftype
        
        for k, v in self.file_type_map.iteritems():
            if k(self.obj):
                return v

        return vfstypes.VFSTypeUnknown()
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _set_attributes(self):
        """
        Set file attibutes
        """

        def set_link_attributes():
            """
            Set appropriate soft link attibutes
            """

            self.info = ""
            self.visual = "-> %s" % self.obj.linkname or ""

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.name = self.either(self.parent.name, lambda: self.name)
        self.mtime = self.either(self.parent.mtime, lambda: self.obj.mtime)
        self.size = self.either(self.parent.size, lambda: self.obj.size)
        self.uid = self.either(self.parent.uid, lambda: self.obj.uid)
        self.gid = self.either(self.parent.gid, lambda: self.obj.gid)
        self.mode = mode.Mode(self.either(self.parent.mode.raw,
                                          lambda: self.obj.mode), self.ftype)
        self.visual = "%s%s" % (self.vtype, self.name)
                
        self.info = "%s %s" % (util.format_size(self.size), self.mode)

        if self.is_link():
            set_link_attributes()
        elif self.is_file():
            _mode = stat.S_IMODE(self.mode.raw)

            # Executable
            if _mode & 0111:
                self.vtype = "*"
                self.visual = "*%s" % self.name

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _init_obj(self):
        tarobj = self._open_archive()
        path = self.path.lstrip(os.sep)

        try:
            obj = tarobj.getmember(path)
        except KeyError:
            obj = tarobj.getmember(path + os.sep)
        
        return obj

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _open_archive(self):
        if self.tarobj is not None:
            return self.tarobj
        
        _mode = "r"

        if self.driver == "gztar":
            _mode = "r:gz"
        elif self.driver == "bz2tar":
            _mode = "r:bz2"

        self.tarobj = tarfile.open(self.parent.path, mode=_mode)
        return self.tarobj
                            
