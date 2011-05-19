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

from libxyz.exceptions import XYZRuntimeError
from libxyz.core.utils import ustring
from libxyz.vfs import types as vfstypes
from libxyz.vfs import vfsobj
from libxyz.vfs import util
from libxyz.vfs import mode
from libxyz.ui import BlockEntries

class TarVFSObject(vfsobj.VFSObject):
    """
    Tar archive interface
    """

    def either(self, a, b):
        if self.root:
            return a
        else:
            return b()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    get_name = lambda self, x: os.path.basename(x.name.rstrip(os.path.sep))
    get_path = lambda self, x: os.path.join(self.ext_path, x.lstrip(os.sep))
    get_int_path = lambda self, x: x.lstrip(os.sep)

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
        self.members = None

        super(TarVFSObject, self).__init__(*args, **kwargs)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def walk(self):
        """
        Directory tree walker
        @return: tuple (parent, dir, objects) where:
        parent - parent dir *VFSObject instance
        dir - current dir TarVFSObject instance
        objects - BlockEntries of TarVFSObject objects
        """

        dirs, files = [], []
        self._open_archive()

        for x in self.members.values():
            if self.in_dir(self.path, x.name):
                if x.isdir():
                    dirs.append(x)
                else:
                    files.append(x)

        dirs.sort(cmp=lambda x, y: cmp(self.get_name(x),
                                        self.get_name(y)))
        files.sort(cmp=lambda x, y: cmp(self.get_name(x),
                                         self.get_name(y)))

        if self.path == os.sep:
            _parent = self.xyz.vfs.get_parent(self.parent.full_path, self.enc)
        else:
            _parent = self.xyz.vfs.dispatch(
                self.get_path(os.path.dirname(self.path)), self.enc)
            _parent.name = ".."

        return [
            _parent,
            self,
            BlockEntries(self.xyz, dirs + files,
                         lambda x: self.get_path(x.name))]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def copy(self, path, existcb=None, errorcb=None, save_attrs=True,
             follow_links=False, cancel=None):

        env = {
            'override': 'abort',
            'error': 'abort'
            }

        tarobj = self._open_archive()

        try:
            if self.is_dir():
                f = self._copy_dir
            else:
                f = self._copy_file

            f(self.path, path, existcb, errorcb,
              save_attrs, follow_links, env, cancel, tarobj=tarobj)
        except XYZRuntimeError:
            # Aborted
            return False
        else:
            return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def open(self, mode='r'):
        """
        Open self object in provided mode
        """

        if self.fileobj:
            return self
        else:
            self.fileobj = self.tarobj.extractfile(
                self.get_int_path(self.path))

            return self

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def close(self):
        """
        Close self object
        """

        if self.fileobj is None:
            return
        else:
            try:
                self.fileobj.close()
            finally:
                self.fileobj = None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def read(self, bytes=None):
        """
        Read bytes from self object
        """

        return self.fileobj.read(bytes)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def tell(self):
        """
        Tell file position
        """

        return self.fileobj.tell()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def seek(self, offset, whence=0):
        """
        Perform seek() on object
        """

        return self.fileobj.seek(offset, whence)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _prepare(self):
        if self.path == os.sep:
            self.root = True
        else:
            self.root = False

        (self.tarobj, self.members) = self._find_cached()

        if self.root:
            self.obj = None
        else:
            self.obj = self._init_obj()

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

    def _normalize(self, path):
        """
        Normalize path
        """

        if path.startswith(os.sep):
            return path.lstrip(os.sep)
        else:
            return path

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return "<TarVFSObject object: %s>" % self.path

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

    def _init_obj(self, altpath=None):
        self._open_archive()
        path = (altpath or self.path).lstrip(os.sep)

        try:
            obj = self.members[path]
        except KeyError:
             obj = self.members[path + os.sep]

        return obj

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _open_archive(self):
        if self.tarobj is None:
            _mode = "r"

            if self.driver == "gztar":
                _mode = "r:gz"
            elif self.driver == "bz2tar":
                _mode = "r:bz2"

            self.tarobj = tarfile.open(fileobj=self.parent.open(), mode=_mode)
            self.members = self._init_members(self.tarobj)

            self.xyz.vfs.set_cache(self.parent.full_path, (self.tarobj,
                                                           self.members))

        return self.tarobj

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _copy_file(self, src, dst, existcb, errorcb, save_attrs,
                   follow_links, env, cancel=None, tarobj=None):
        """
        File-to-file copy
        """

        obj = self._init_obj(src)

        if os.path.exists(dst) and os.path.isdir(dst):
            dstto = os.path.join(dst, os.path.basename(src))
        else:
            dstto = dst

        if os.path.exists(dstto):
            if env['override'] not in ('override all', 'skip all'):
                if existcb:
                    try:
                        env['override'] = existcb(
                            self.xyz.vfs.dispatch(dstto))
                    except Exception:
                        env['override'] = 'abort'

            if env['override'] == 'abort':
                raise XYZRuntimeError()
            elif env['override'] in ('skip', 'skip all'):
                return False

        try:
            if not follow_links and obj.issym():
                os.symlink(obj.linkname, dstto)
            else:
                if obj.issym():
                    objdir = os.path.dirname(obj.name)
                    src = os.path.join(objdir, obj.linkname)

                self._do_copy(src, dstto, save_attrs, tarobj, obj)

            return True
        except Exception, e:
            if env['error'] != 'skip all':
                if errorcb:
                    try:
                        env['error'] = errorcb(
                            self.xyz.vfs.dispatch(self.full_path), str(e))
                    except Exception:
                        env['error'] = 'abort'

                if env['error'] == 'abort':
                    raise XYZRuntimeError()

        return False

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _copy_dir(self, src, dst, existcb, errorcb, save_attrs,
                  follow_links, env, cancel=None, tarobj=None):
        """
        Dir-to-dir copy
        """

        obj = self._init_obj(src)

        if os.path.exists(dst) and os.path.isdir(dst) and \
               os.path.basename(src) != os.path.basename(dst):
            dst = os.path.join(dst, os.path.basename(src))

        if not follow_links and obj.issym():
            os.symlink(obj.linkname, dst)

            return True

        if obj.isdir() and not os.path.exists(dst):
            os.makedirs(dst)

        files = [x for x in tarobj.getmembers() if
                 self.in_dir(obj.name, x.name)]

        for f in files:
            if cancel is not None and cancel.isSet():
                raise StopIteration()

            srcobj = f.name
            dstobj = os.path.join(dst, self.get_name(f))

            if self._init_obj(srcobj).isdir():
                fun = self._copy_dir
            else:
                fun = self._copy_file

            fun(srcobj, dstobj, existcb, errorcb, save_attrs,
                follow_links, env, cancel, tarobj)

        if obj.isdir() and save_attrs:
            self._copystat(obj, dst)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _do_copy(self, src, dst, save_attrs, tarobj, obj):
        """
        Copy file from inside archive
        """

        fsrc = tarobj.extractfile(self._normalize(src))

        fdst = open(dst, "w")

        while True:
            block = fsrc.read(4096)

            # EOF
            if block == '':
                break

            fdst.write(block)

        fsrc.close()
        fdst.close()

        if save_attrs:
            self._copystat(obj, dst)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _copystat(self, obj, dst):
        try:
            os.chown(dst, obj.uid, obj.gid)
        except Exception, e:
            xyzlog.warning(_(u"Unable to chown %s: %s") %
                           (ustring(dst), unicode(e)))

        try:
            os.chmod(dst, obj.mode)
        except Exception, e:
            xyzlog.warning(_(u"Unable to chmod %s: %s") %
                           (ustring(dst), unicode(e)))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _find_cached(self):
        """
        Find cached data
        """

        return self.xyz.vfs.get_cache(self.parent.full_path) or (None, None)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _init_members(self, tarobj):
        """
        Init members from archive contents
        """

        members = {}

        for name in tarobj.getnames():
            data = util.split_path(name)
            current = []

            for obj in data:
                current.append(obj)

                path = os.path.join(*current)

                if path not in members:
                    try:
                        item = tarobj.getmember(path)
                    except KeyError:
                        try:
                            item = tarobj.getmember(path + os.sep)
                        except KeyError:
                            # Create dummy dir
                            item = self._make_dummy_dir(path)

                    members[path] = item

        return members

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _make_dummy_dir(self, name):
        """
        Make dummy directory object
        """

        uid = os.getuid()
        gid = os.getgid()

        obj = tarfile.TarInfo(name)
        obj.type = tarfile.DIRTYPE
        obj.mode = 0755
        obj.uid = uid
        obj.gid = gid
        obj.mtime = int(time.time())
        obj.uname = util.get_user(uid)
        obj.gname = util.get_group(gid)

        return obj
