#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
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

from libxyz.vfs import types as vfstypes

def get_file_type(st_mode):
    """
    Find out file type
    @param st_mode: Raw st_mode obtained from os.stat()
    """

    _types = (
              (stat.S_ISDIR,  vfstypes.VFSTypeDir),
              (stat.S_ISCHR,  vfstypes.VFSTypeChar),
              (stat.S_ISBLK,  vfstypes.VFSTypeBlock),
              (stat.S_ISREG,  vfstypes.VFSTypeFile),
              (stat.S_ISFIFO, vfstypes.VFSTypeFifo),
              (stat.S_ISLNK,  vfstypes.VFSTypeLink),
              (stat.S_ISSOCK, vfstypes.VFSTypeSocket),
              )

    for _test, _type in _types:
        if _test(st_mode):
            return _type()

    return vfstypes.VFSTypeUnknown()
