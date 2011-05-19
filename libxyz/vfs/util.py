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

import stat
import os
import pwd
import grp

from libxyz.vfs import types as vfstypes

_types = (
          (stat.S_ISDIR,  vfstypes.VFSTypeDir),
          (stat.S_ISCHR,  vfstypes.VFSTypeChar),
          (stat.S_ISBLK,  vfstypes.VFSTypeBlock),
          (stat.S_ISREG,  vfstypes.VFSTypeFile),
          (stat.S_ISFIFO, vfstypes.VFSTypeFifo),
          (stat.S_ISLNK,  vfstypes.VFSTypeLink),
          (stat.S_ISSOCK, vfstypes.VFSTypeSocket),
          )

_types2 = {"d": vfstypes.VFSTypeDir,
           "c": vfstypes.VFSTypeChar,
           "b": vfstypes.VFSTypeBlock,
           "-": vfstypes.VFSTypeFile,
           "p": vfstypes.VFSTypeFifo,
           "l": vfstypes.VFSTypeLink,
           "s": vfstypes.VFSTypeSocket,
          }

def get_file_type(st_mode):
    """
    Find out file type
    @param st_mode: Raw st_mode obtained from os.stat()
                    or one char string as the first char in ls -l output
    """

    global _types, _types2

    if isinstance(st_mode, basestring):
        return _types2.get(st_mode, vfstypes.VFSTypeUnknown)()

    for _test, _type in _types:
        if _test(st_mode):
            return _type()

    return vfstypes.VFSTypeUnknown()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def format_size(size):
    """
    Format file-object size
    """

    _s = long(size)

    _data = (
             (1024 * 1024 * 1024, u"G", lambda x, y: u"%.2f" % (float(x) / y)),
             (1024 * 1024, u"M", lambda x, y: unicode(x / y)),
             (1024, u"K", lambda x, y: unicode(x / y)),
             )

    for _size, _suffix, _func in _data:
        if _s >= _size:
            return u"%s%s" % (_func(_s, _size), _suffix)

    return size

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def split_path(path):
    return [x for x in path.split(os.sep) if x]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_user(uid=None):
    """
    Get user name by UID

    @param uid: User ID
    @return: username or None
    """

    if uid is None:
        uid = os.getuid()

    try:
        name = pwd.getpwuid(uid).pw_name
    except (KeyError, TypeError):
        name = None

    return name

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_group(gid=None):
    """
    Get group name by GID

    @param gid: Group ID
    @return: group name or None
    """

    if gid is None:
        gid = os.getuid()

    try:
        name = grp.getgrgid(gid).gr_name
    except (KeyError, TypeError):
        name = None

    return name
