#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <syhpoon@syhpoon.name> 2008-2011
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

import subprocess
import re
import os
import stat
import time

import libxyz

from libxyz.exceptions import XYZRuntimeError
from libxyz.core.utils import ustring
from libxyz.vfs import types as vfstypes
from libxyz.vfs import vfsobj
from libxyz.vfs import util
from libxyz.vfs import mode
from libxyz.ui import BlockEntries

# [YY]YY/MM/DD hh:mm[:ss]
DATETIME_PAT1 = r"(?:\d{2,4}\/\d{2}\/\d{2}\s+"\
                r"\d{1,2}:\d{1,2}(?:\:\d{1,2})?)"

# MM/DD/YYYY hh:mm[:ss]
DATETIME_PAT2 = r"(?:\d{2}\/\d{2}\/\d{4}\s+"\
                r"\d{1,2}:\d{1,2}(?:\:\d{1,2})?)"

OBJ_PAT = re.compile(r"^" \
                     r"(?P<mode>\S+)\s+" \
                     r"(?P<links>\d+)\s+" \
                     r"(?P<uid>\S+)\s+" \
                     r"(?P<gid>\S+)\s+" \
                     r"(?P<size>\d+)\s+" \
                     r"(?P<dtime>%s)\s+" \
                     r"(?P<path>.+?)" \
                     r"(?:\s+\-\>\s+(?P<link>.+?))?$" %
                     "|".join([DATETIME_PAT1, DATETIME_PAT2]),
                     re.UNICODE)

class ExternalVFSObject(vfsobj.VFSObject):
    """
    External VFS interface
    """

    get_name = lambda self, x: os.path.basename(x["path"].rstrip(os.path.sep))
    get_path = lambda self, x: os.path.join(self.ext_path, x.lstrip(os.sep))
    obj_pat = OBJ_PAT

    def __init__(self, *args, **kwargs):
        super(ExternalVFSObject, self).__init__(*args, **kwargs)

        self.members = []
        self.obj = None
        self.path_sel = libxyz.PathSelector()
        self.driver_cmd = self._init_driver_cmd(self.driver)

        # Check if we've already visited this particular VFS object
        _cache = self.xyz.vfs.get_cache(self.parent.full_path)

        # First time visit, we should run driver and build members list then
        if _cache is None:
            self.members = dict([self._parse_obj(x) for x in 
                                 self._run_driver("list",
                                                  self.parent.full_path) if x])

            # Now cache the data for further use
            self.xyz.vfs.set_cache(self.parent.full_path, self.members)
        else:
            self.members = _cache

        # We're at the root of VFS
        if self.path == os.sep:
            self.root = True
            self.ftype = self.parent.ftype
        # Otherwise we're somewhere inside, strip the leading slash from path
        else:
            self.root = False
            self.path = self.path.lstrip(os.sep)
            self.obj = self._init_obj(self.path)
            self.ftype = self.obj["type"]

        self.vtype = self.ftype.vtype

        self._set_attributes()

        self.attributes = (
            (_(u"Name"), ustring(self.name)),
            (_(u"Type"), ustring(self.ftype)),
            (_(u"Modification time"), ustring(self.mtime)),
            (_(u"Size in bytes"), ustring(self.size)),
            (_(u"Owner"), ustring(self.uid)),
            (_(u"Group"), ustring(self.gid)),
            (_(u"Access mode"), ustring(self.mode)),
            (_(u"Type-specific data"), self.data),
            )
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def either(self, a, b):
        if self.root:
            return a
        else:
            return b()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def walk(self):
        """
        Directory tree walker
        @return: tuple (parent, dir, objects) where:
        parent - parent dir *VFSObject instance
        dir - current dir ExternalVFSObject instance
        objects - BlockEntries of ExternalVFSObject objects
        """

        dirs, files = [], []

        for x in self.members.values():
            if self.in_dir(self.path, x["path"]):
                if isinstance(x["type"], vfstypes.VFSTypeDir):
                    dirs.append(x)
                else:
                    files.append(x)

        dirs.sort(cmp=lambda x, y: cmp(self.get_name(x), self.get_name(y)))
        files.sort(cmp=lambda x, y: cmp(self.get_name(x), self.get_name(y)))

        if self.root:
            _parent = self.xyz.vfs.get_parent(self.parent.full_path, self.enc)
        else:
            _parent = self.xyz.vfs.dispatch(
                self.get_path(os.path.dirname(self.path)), self.enc)
            _parent.name = ".."

        return [
            _parent,
            self,
            BlockEntries(self.xyz, dirs + files,
                         lambda x: self.get_path(x["path"]))]

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

            f(self.path, path, existcb, errorcb,
              save_attrs, follow_links, env, cancel)
        except XYZRuntimeError:
            # Aborted
            return False
        else:
            return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _copy_file(self, src, dst, existcb, errorcb, save_attrs,
                   follow_links, env, cancel=None):
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
            self._run_driver("copyout", self.parent.full_path, src, dstto)

            if save_attrs:
                self._copystat(obj, dstto)

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
                  follow_links, env, cancel=None):
        """
        Dir-to-dir copy
        """

        obj = self._init_obj(src)

        if os.path.exists(dst) and os.path.isdir(dst) and \
               os.path.basename(src) != os.path.basename(dst):
            dst = os.path.join(dst, os.path.basename(src))

        if isinstance(obj["type"], vfstypes.VFSTypeDir) \
               and not os.path.exists(dst):
            os.makedirs(dst)

        files = [x for x in self.members.values() if self.in_dir(obj["path"],
                                                                 x["path"])]

        for f in files:
            if cancel is not None and cancel.isSet():
                raise StopIteration()

            srcobj = f["path"]
            dstobj = os.path.join(dst, self.get_name(f))

            if isinstance(f["type"], vfstypes.VFSTypeDir):
                fun = self._copy_dir
            else:
                fun = self._copy_file

            fun(srcobj, dstobj, existcb, errorcb, save_attrs,
                follow_links, env, cancel)

        if isinstance(obj["type"], vfstypes.VFSTypeDir) and save_attrs:
            self._copystat(obj, dst)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _run_driver(self, cmd, *args):
        """
        Try to execute driver on archive
        """

        try:
            return subprocess.Popen(
                [self.driver_cmd, cmd] + list(args),
                stdout=subprocess.PIPE).communicate()[0].split("\n")
        except Exception, e:
            raise XYZRuntimeError(_(u"Error executing VFS driver %s: %s") %
                                  (self.driver_cmd, unicode(e)))

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
            self.visual = "-> %s" % self.obj["link"]

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.name = self.either(self.parent.name, lambda: self.name)
        self.mtime = self.either(self.parent.mtime,
                                 lambda: self.obj["datetime"])
        self.size = self.either(self.parent.size, lambda: self.obj["size"])
        self.uid = self.either(self.parent.uid, lambda: self.obj["uid"])
        self.gid = self.either(self.parent.gid, lambda: self.obj["gid"])
        self.mode = mode.Mode(
            self.either(self.parent.mode.raw,
                        lambda: mode.Mode.string_to_raw(self.obj["mode"])),
                        self.ftype)
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
        
    def __str__(self):
        return "<ExternalVFSObject instance: %s>" % self.path

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _parse_obj(self, raw):
        """
        Parse raw object string returned by list command
        """

        parsed = self.obj_pat.match(raw)

        if parsed is None:
            raise XYZRuntimeError(
                _(u"External VFS: error parsing driver output: %s") % raw)

        return (parsed.group("path"),
                {
                    "mode": parsed.group("mode"),
                    "links": int(parsed.group("links")),
                    "uid": self._parse_id(parsed.group("uid")),
                    "gid": self._parse_id(parsed.group("gid")),
                    "size": int(parsed.group("size")),
                    "datetime": parsed.group("dtime"),
                    "path": parsed.group("path"),
                    "link": parsed.group("link"),
                    "type": util.get_file_type(parsed.group("mode")[0])
                    })

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _init_driver_cmd(self, driver):
        _sys, _usr = self.path_sel.get_vfs_driver(self.driver)

        driver_cmd = self.path_sel.get_first_of([_sys, _usr])

        if driver_cmd is None:
            raise XYZRuntimeError(
                _(u"Driver for '%s' external VFS does not exist") % driver)
        else:
            return driver_cmd

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def  _init_obj(self, path):
        """
        Try to find info for provided path
        """

        try:
            return self.members[path]
        except KeyError:
            return self.members[path + os.sep]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _copystat(self, obj, dst):
        try:
            os.chown(dst, obj["uid"], obj["gid"])
        except Exception, e:
            xyzlog.warning(_(u"Unable to chown %s: %s") %
                           (ustring(dst), unicode(e)))

        try:
            os.chmod(dst, mode.Mode.string_to_raw(obj["mode"]))
        except Exception, e:
            xyzlog.warning(_(u"Unable to chmod %s: %s") %
                           (ustring(dst), unicode(e)))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _parse_id(self, id):
        """
        Try to parse provided id as either numeric ID or username/groupname
        """

        try:
            return int(id)
        except ValueError:
            return id
