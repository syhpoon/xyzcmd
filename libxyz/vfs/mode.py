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

from libxyz.vfs import util

class Mode(object):
    """
    A stat st_mode field representaion
    """

    def __init__(self, st_mode, vfstype):
        """
        @param st_mode: Raw st_mode obtained from os.stat()
        @param vfstype: VFS file type
        """

        self.raw = st_mode
        self.vfstype = vfstype
        self.string = self._make_string_mode()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return self.string

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __repr__(self):
        return self.__str__()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _make_string_mode(self):
        """
        Make string mode representaion
        """

        _str_mode = [self.vfstype.str_type]

        # usr bits
        _str_mode.extend(self._usr_bits())

        # group bits
        _str_mode.extend(self._grp_bits())

        # other bits
        _str_mode.extend(self._oth_bits())

        return u"".join(_str_mode)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _usr_bits(self):
        _raw = self.raw
        _str_mode = []

        if _raw & stat.S_IRUSR:
            _bit = u"r"
        else:
            _bit = u"-"
        _str_mode.append(_bit)

        if _raw & stat.S_IWUSR:
            _bit = u"w"
        else:
            _bit = u"-"
        _str_mode.append(_bit)

        _o_mode = _raw & (stat.S_IXUSR | stat.S_ISUID)

        if _o_mode == 0:
            _bit = u"-"
        elif _o_mode == stat.S_IXUSR:
            _bit = u"x"
        elif _o_mode == stat.S_ISUID:
            _bit = u"S"
        elif _o_mode == stat.S_IXUSR | stat.S_ISUID:
            _bit = u"s"
        _str_mode.append(_bit)

        return _str_mode

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _grp_bits(self):
        _raw = self.raw
        _str_mode = []

        if _raw & stat.S_IRGRP:
            _bit = u"r"
        else:
            _bit = u"-"
        _str_mode.append(_bit)

        if _raw & stat.S_IWGRP:
            _bit = u"w"
        else:
            _bit = u"-"
        _str_mode.append(_bit)

        _o_mode = _raw & (stat.S_IXGRP | stat.S_ISGID)

        if _o_mode == 0:
            _bit = u"-"
        elif _o_mode == stat.S_IXGRP:
            _bit = u"x"
        elif _o_mode == stat.S_ISGID:
            _bit = u"S"
        elif _o_mode == stat.S_IXGRP | stat.S_ISGID:
            _bit = u"s"
        _str_mode.append(_bit)

        return _str_mode

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _oth_bits(self):
        _raw = self.raw
        _str_mode = []

        if _raw & stat.S_IROTH:
            _bit = u"r"
        else:
            _bit = u"-"
        _str_mode.append(_bit)

        if _raw & stat.S_IWOTH:
            _bit = u"w"
        else:
            _bit = u"-"
        _str_mode.append(_bit)

        _o_mode = _raw & (stat.S_IXOTH | stat.S_ISVTX)

        if _o_mode == 0:
            _bit = u"-"
        elif _o_mode == stat.S_IXOTH:
            _bit = u"x"
        elif _o_mode == stat.S_ISVTX:
            _bit = u"T"
        elif _o_mode == stat.S_IXOTH | stat.S_ISVTX:
            _bit = u"t"
        _str_mode.append(_bit)

        return _str_mode
