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
import os.path
import stat
import time
import tarfile

from libxyz.vfs import types as vfstypes

from libxyz.vfs import vfsobj
from libxyz.vfs import util
from libxyz.vfs import mode
from libxyz.vfs import local
from libxyz.core.utils import ustring

class TarVFSObject(vfsobj.VFSObject):
    """
    Access GNU Tar archives
    """

    def walk(self):
        """
        Directory tree walker
        @return: tuple (parent, dir, dirs, files) where:
        parent - parent dir *VFSFile instance
        dir - current dir TarVFSFile instance
        dirs - list of TarVFSFile objects of directories
        files - list of TarVFSFile objects of files
        """
        
        def in_dir(d, e):
            """
            Filter only those archive entries which exist in the same
            directory level
            """

            return True if e.startswith(d.lstrip(os.sep)) and \
                   len(util.split_path(e)) == (len(util.split_path(d)) + 1) \
                   else False

        name = lambda x: os.path.basename(x.name)
        get_path = lambda x: os.sep.join([self.full_path, x])
        
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        tarobj = tarfile.open(self.path)
        entries = tarobj.getmembers()

        _dirs = [x for x in entries if x.isdir() and
                 in_dir(self.int_path, x.name)]
        _files = [x for x in entries if not x.isdir() and
                  in_dir(self.int_path, x.name)]

        _dirs.sort(cmp=lambda x, y: cmp(name(x), name(y)))
        _files.sort(cmp=lambda x, y: cmp(name(x), name(y)))

        self.xyz.vfs.get_file_by_path(self.full_path)
        
        _parent = local.LocalVFSFile(os.path.dirname(self.path), self.enc)
        _parent.name = u".."

        if not isinstance(_parent.ftype, vfstypes.VFSTypeLink):
            _parent.visual = u"/.."

        return [
            _parent,
            self,
            [TarVFSFile(get_path(name(x)), self.enc, x) for x in _dirs],
            [TarVFSFile(get_path(name(x)), self.enc, x) for x in _files],
            ]

#++++++++++++++++++++++++++++++++++++++++++++++++

class TarVFSFile(vfsobj.VFSFile):
    """
    Tar archive file object
    """

    def __init__(self, path, enc, obj):
        self._file_type_map = {obj.isfile: vfstypes.VFSTypeFile(),
                               obj.isdir: vfstypes.VFSTypeDir(),
                               obj.issym: vfstypes.VFSTypeLink(),
                               obj.ischr: vfstypes.VFSTypeChar(),
                               obj.isblk: vfstypes.VFSTypeBlock(),
                               obj.isfifo: vfstypes.VFSTypeFifo(),
                               }
        
        super(TarVFSFile, self).__init__(path, enc, obj)

        self.ftype = self._find_type()
        self.vtype = self.ftype.vtype

        self._set_attributes()

        self.attributes = (
            (_(u"Name"), self.name),
            (_(u"Type"), self.ftype),
            (_(u"Modification time"), ustring(time.ctime(self.mtime))),
            (_(u"Size in bytes"), ustring(self.size)),
            (_(u"Owner"), self.obj.uname),
            (_(u"Group"), self.obj.gname),
            (_(u"Access mode"), ustring(self.mode)),
            (_(u"Type-specific data"), self.data),
            )

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return "<TarVFSFile object: %s>" % self.path

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __repr__(self):
        return self.__str__()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _find_type(self):
        """
        Find out file type
        """

        for k, v in self._file_type_map.iteritems():
            if k():
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

            self.info = u""
            self.visual = "-> %s" % obj.linkname or ""

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.mtime = self.obj.mtime
        self.size = self.obj.size
        self.uid = self.obj.uid
        self.gid = self.obj.gid
        self.mode = mode.Mode(self.obj.mode, self.ftype)
        self.visual = u"%s%s" % (self.vtype, self.name)
                
        self.info = u"%s %s" % (util.format_size(self.size), self.mode)

        if isinstance(self.ftype, vfstypes.VFSTypeLink):
            set_link_attributes()
        elif isinstance(self.ftype, vfstypes.VFSTypeFile):
            _mode = stat.S_IMODE(self.mode.raw)

            # Executable
            if _mode & 0111:
                self.vtype = u"*"
                self.visual = u"*%s" % self.name
