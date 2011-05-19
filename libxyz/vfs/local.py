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
import stat
import time
import shutil
import errno

from libxyz.exceptions import VFSError
from libxyz.exceptions import XYZRuntimeError
from libxyz.exceptions import XYZValueError
from libxyz.vfs import vfsobj
from libxyz.vfs import types
from libxyz.vfs import util
from libxyz.vfs import mode
from libxyz.core.utils import ustring, bstring
from libxyz.ui import BlockEntries

def ensure_opened(func):
    def wrap(self, *args, **kwargs):
        if self.fileobj is None:
            raise VFSError(_(u"Object must be opened before any operation"))
        else:
            return func(self, *args, **kwargs)

    return wrap

class LocalVFSObject(vfsobj.VFSObject):
    """
    Local VFS object is used to access local filesystem
    """

    def __init__(self, *args, **kwargs):
        super(LocalVFSObject, self).__init__(*args, **kwargs)

        self.ftype = self._find_type(self.path)
        self.vtype = self.ftype.vtype

        self._set_attributes()

        _time = lambda x: ustring(time.ctime(x))

        self.attributes = (
            (_(u"Name"), ustring(self.name)),
            (_(u"Type"), ustring(self.ftype)),
            (_(u"Access time"), _time(self.atime)),
            (_(u"Modification time"), _time(self.mtime)),
            (_(u"Change time"), _time(self.ctime)),
            (_(u"Size in bytes"), ustring(self.size)),
            (_(u"Owner"), ustring(self._uid(self.uid))),
            (_(u"Group"), ustring(self._gid(self.gid))),
            (_(u"Access mode"), ustring(self.mode)),
            (_(u"Inode"), ustring(self.inode)),
            (_(u"Type-specific data"), self.data),
            )

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def walk(self):
        """
        Directory tree walker
        @return: tuple (parent, dir, objects) where:
                 parent - parent dir LocalVFSObject instance
                 dir - current LocalVFSObject instance
                 objects - BlockEntries of LocalVFSObject objects
        """

        try:
            _dir, _dirs, _files = os.walk(self.path).next()
        except StopIteration:
            raise XYZRuntimeError(_(u"Unable to walk on %s") %
                                  ustring(self.path))

        _dirs.sort()
        _files.sort()

        _parent = self.xyz.vfs.get_parent(_dir, self.enc)

        get_path = lambda x: os.path.abspath(os.path.join(self.path, x))

        return [_parent, self,
                BlockEntries(self.xyz, _dirs + _files, get_path)]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def remove(self, recursive=True):
        """
        [Recursively] remove object
        """

        if self.is_dir():
            if recursive:
                shutil.rmtree(self.path)
            else:
                os.rmdir(self.path)
        else:
            os.unlink(self.path)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def mkdir(self, newdir):
        """
        Create new dir inside object (only valid for directory object types)
        """

        if not (self.is_dir() or
                (self.is_link() and self.data.is_dir())):
            raise XYZValueError(
                _(u"Unable to create directory inside %s object type") %
                self.ftype)
        else:
            os.mkdir(newdir)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def copy(self, path, existcb=None, errorcb=None, save_attrs=True,
             follow_links=False, cancel=None):

        env = {
            'override': 'abort',
            'error': 'abort'
            }

        try:
            if self.is_dir():
                f = self._copy_dir
            else:
                f = self._copy_file

            f(self.full_path, path, existcb, errorcb,
              save_attrs, follow_links, env, cancel)
        except XYZRuntimeError:
            # Aborted
            return False
        else:
            return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def move(self, path, existcb=None, errorcb=None, save_attrs=True,
             follow_links=False, cancel=None):
        """
        Move object
        """

        def _handle_error(e, obj):
            if env['error'] != 'skip all':
                if errorcb:
                    try:
                        env['error'] = errorcb(obj, str(e))
                    except Exception:
                        env['error'] = 'abort'

            if env['error'] == 'abort':
                raise XYZRuntimeError()

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def _move_file(src, dst, *args, **kwargs):
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
                os.rename(src, dstto)

                return True
            except OSError, e:
                # Cross-device link, try to copy
                if e.errno == errno.EXDEV:
                    if self._copy_file(src, dst, *args, **kwargs):
                        # Remove after successfully copied
                        try:
                            os.unlink(src)
                        except Exception, e2:
                            _handle_error(e2, self.xyz.vfs.dispatch(src))
                else:
                    _handle_error(e, self.xyz.vfs.dispatch(src))
            except XYZRuntimeError:
                raise
            except Exception, e3:
                _handle_error(e3, self.xyz.vfs.dispatch(src))

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def _move_dir(src, dst, *args, **kwargs):
            if os.path.exists(dst) and os.path.isdir(dst) and \
                   os.path.basename(src) != os.path.basename(dst):
                dst = os.path.join(dst, os.path.basename(src))

            if os.path.isdir(src) and not os.path.exists(dst):
                os.makedirs(dst)

            files = os.listdir(src)

            cancel = kwargs.get('cancel', None)

            for f in files:
                if cancel is not None and cancel.isSet():
                    raise StopIteration()

                srcobj = os.path.join(src, f)
                dstobj = os.path.join(dst, f)

                if os.path.isdir(srcobj):
                    fun = _move_dir
                else:
                    fun = _move_file

                fun(srcobj, dstobj, *args, **kwargs)

            try:
                os.rmdir(src)
            except Exception, e:
                _handle_error(e, self.xyz.vfs.dispatch(src))

            return True

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        env = {
            'override': 'abort',
            'error': 'abort'
            }

        try:
            if self.is_dir():
                fun = _move_dir
            else:
                fun = _move_file

            fun(self.full_path, path, existcb, errorcb, save_attrs,
                follow_links, env, cancel=cancel)
        except XYZRuntimeError:
            # Aborted
            return False

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def open(self, mode='r'):
        """
        Open self object in provided mode
        """

        if self.fileobj:
            return self
        else:
            self.fileobj = open(self.path, mode)

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

    @ensure_opened
    def read(self, bytes=None):
        """
        Read bytes from self object
        """

        return self.fileobj.read(bytes)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @ensure_opened
    def tell(self):
        """
        Tell file position
        """

        return self.fileobj.tell()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @ensure_opened
    def seek(self, offset, whence=0):
        """
        Perform seek() on object
        """

        return self.fileobj.seek(offset, whence)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## Internal stuff

    def __str__(self):
        return "<LocalVFSObject object: %s>" % self.path

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _uid(self, uid):
        _name = util.get_user(uid)

        if _name is not None:
            return "%s (%s)" % (bstring(uid), _name)
        else:
            return bstring(uid)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _gid(self, gid):
        _name = util.get_group(gid)

        if _name is not None:
            return "%s (%s)" % (bstring(gid), _name)
        else:
            return bstring(gid)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _find_type(self, path):
        """
        Find out file type
        """

        try:
            self._stat = os.lstat(path)
        except OSError, e:
            raise VFSError(_(u"Unable to stat file %s: %s") %
                           (ustring(path), unicode(e.strerror, xyzenc)))

        return util.get_file_type(self._stat.st_mode)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _set_attributes(self):
        """
        Set file attibutes
        """

        def set_link_attributes():
            """
            Set appropriate soft link attibutes
            """

            _realpath = os.readlink(self.path)
            _fullpath = os.path.realpath(self.path)

            if not os.path.exists(_fullpath):
                self.vtype = "!"
            else:
                try:
                    self.data = self.xyz.vfs.dispatch(_fullpath, self.enc)
                except VFSError, e:
                    xyzlog.error(_(u"Error creating VFS object: %s") %
                                 unicode(e))
                else:
                    if isinstance(self.data.ftype, types.VFSTypeDir):
                        self.vtype = "~"
            self.info = ""
            self.visual = "-> %s" % _realpath

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def set_char_attributes():
            """
            Set appropriate character device attibutes
            """

            _dev = self._stat.st_rdev
            self.info = "%s, %s %s" % (os.major(_dev), os.minor(_dev),
                                       self.mode)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.atime = self._stat.st_atime
        self.mtime = self._stat.st_mtime
        self.ctime = self._stat.st_ctime
        self.size = self._stat.st_size
        self.uid = self._stat.st_uid
        self.gid = self._stat.st_gid
        self.inode = self._stat.st_ino
        self.mode = mode.Mode(self._stat.st_mode, self.ftype)
        self.visual = "%s%s" % (self.vtype, self.name)
        self.info = "%s %s" % (util.format_size(self.size), self.mode)

        if self.is_link():
            set_link_attributes()
        elif self.is_char():
            set_char_attributes()
        elif self.is_file():
            _mode = stat.S_IMODE(self.mode.raw)

            # Executable
            if _mode & 0111:
                self.vtype = "*"
                self.visual = "*%s" % self.name

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _copy_file(self, src, dst, existcb, errorcb, save_attrs,
                   follow_links, env, cancel=None):
        """
        File-to-file copy
        """

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
            if not follow_links and os.path.islink(src):
                linkto = os.readlink(src)
                os.symlink(linkto, dstto)
            else:
                if save_attrs:
                    fun = shutil.copy2
                else:
                    fun = shutil.copyfile

                fun(src, dstto)

            return True
        except Exception, e:
            if env['error'] != 'skip all':
                if errorcb:
                    try:
                        env['error'] = errorcb(
                            self.xyz.vfs.dispatch(src), str(e))
                    except Exception:
                        env['error'] = 'abort'

                if env['error'] == 'abort':
                    raise XYZRuntimeError()

        return False

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _copy_dir(self, src, dst, existcb, errorcb, save_attrs,
                  follow_links, env, cancel=None):
        """
        Dir-to-dir copy
        """

        if os.path.exists(dst) and os.path.isdir(dst) and \
               os.path.basename(src) != os.path.basename(dst):
            dst = os.path.join(dst, os.path.basename(src))

        if not follow_links and os.path.islink(src):
            linkto = os.readlink(src)
            os.symlink(linkto, dst)

            return True

        if os.path.isdir(src) and not os.path.exists(dst):
            os.makedirs(dst)

        files = os.listdir(src)

        for f in files:
            if cancel is not None and cancel.isSet():
                raise StopIteration()

            srcobj = os.path.join(src, f)
            dstobj = os.path.join(dst, f)

            if os.path.isdir(srcobj):
                fun = self._copy_dir
            else:
                fun = self._copy_file

            fun(srcobj, dstobj, existcb, errorcb, save_attrs,
                follow_links, env, cancel)

        if os.path.isdir(src) and save_attrs:
            shutil.copystat(src, dst)
