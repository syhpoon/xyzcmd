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

import os
import re
import types

from libxyz.exceptions import ParseError, SkinError, XYZValueError
from libxyz.parser import BlockParser
from libxyz.parser import FlatParser
from libxyz.parser import MultiParser
from libxyz.parser import ParsedData

import libxyz.ui as uilib

class Skin(object):
    """
    Skin object. Provides simple interface to defined skin rulesets.
    """

    def __init__(self, path):
        """
        @param path: Path to skin file
        """

        if not os.access(path, os.R_OK):
            raise SkinError(_(u"Unable to open skin file for reading"))
        else:
            self.path = path

        self._data = {}

        # Default fallback palette
        self._default = uilib.colors.Palette(u"default",
                        uilib.colors.Foreground(u"DEFAULT"),
                        uilib.colors.Background(u"DEFAULT"),
                        uilib.colors.Monochrome(u"DEFAULT"))

        # 1. Parse
        self._data = self._parse()

        # 2. Order parsed data
        self._check()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return u"<Skin object: %s>" % str(self.path)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __repr__(self):
        return self.__str__()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __getitem__(self, key):
        return self._data[key]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _parse(self):
        def palette_validator(block, var, val):
            """
            Make L{libxyz.ui.colors.Palette} object of palette definition
            """

            _p = self._default.copy()

            if type(val) in types.StringTypes:
                _val = (val,)
            else:
                _val = [x.strip() for x in val]

            _p.fg = uilib.colors.Foreground(_val[0])

            if len(_val) > 1:
                _p.bg = uilib.colors.Background(_val[1])
            if len(_val) > 2:
                _p.ma = tuple([uilib.colors.Monochrome(x) for x in _val[2:]])

            _p.name = self._make_name(block, var)

            return _p

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def priority_validator(block, var, val):
            """
            Validator for priority values (int)
            """

            try:
                return int(val)
            except ValueError, e:
                raise XYZValueError(_(u"Invalid literal for number"))

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # Prepare parsers

        _fs_type_opt = {u"count": 1,
                        u"value_validator": palette_validator,
                        u"validvars": (u"file", u"dir", u"block", u"char",
                                       u"link", u"fifo", u"socket"),
                        }
        _fs_type_p = BlockParser(_fs_type_opt)

        _fs_perm_opt = {u"count": 1,
                        u"value_validator": palette_validator,
                        u"varre": re.compile(r"^\+?\d{4}$"),
                       }
        _fs_perm_p = BlockParser(_fs_perm_opt)

        _fs_owner_opt = {u"count": 1,
                         u"value_validator": palette_validator,
                         u"varre": re.compile(r"^(\w+)?(:(\w+))?$"),
                         }
        _fs_owner_p = BlockParser(_fs_owner_opt)

        _fs_regexp_opt = {u"count": 1,
                          u"value_validator": palette_validator,
                          u"varre": re.compile(r".+"),
                         }
        _fs_regexp_p = BlockParser(_fs_regexp_opt)

        _fs_priority_opt = {u"count": 1,
                            u"value_validator": priority_validator,
                            u"validvars": (u"type",
                                           u"perm", u"regexp", u"owner"),
                            }
        _fs_priority_p = BlockParser(_fs_priority_opt)

        _ui_opt = {u"count": 1,
                   u"value_validator": palette_validator,
                   }
        _ui_p = BlockParser(_ui_opt)

        _flat_opt = {u"count": 1}
        _flat_p = FlatParser(_flat_opt)

        _parsers = {u"fs.type": _fs_type_p,
                    u"fs.perm": _fs_perm_p,
                    u"fs.owner": _fs_owner_p,
                    u"fs.regexp": _fs_regexp_p,
                    u"fs.priority": _fs_priority_p,
                    re.compile(r"ui\.(\w)+"): _ui_p,
                    (u"AUTHOR", u"VERSION", u"DESCRIPTION"): _flat_p,
                    }

        _multi_opt = {u"tokens": (":",)}
        _multi_p = MultiParser(_parsers, _multi_opt)

        _skinfile = open(self.path, "r")

        try:
            _data = _multi_p.parse(_skinfile)
        except ParseError, e:
            raise SkinError(_(u"Error parsing skin file: %s" % str(e)))
        finally:
            _skinfile.close()

        return _data

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _make_name(self, block, resource):
        return "%s@%s" % (resource, block)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _check(self):
        for _required in (u"AUTHOR", u"DESCRIPTION", u"VERSION"):
            if _required not in self._data:
                raise SkinError(_(u"Missing required variable: %s" % _required))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_palette_list(self):
        """
        Return list of defined palettes.
        It is usually passed to register_palette() function
        """

        _list = [self._default.get_palette()]

        for _name, _pdata in self._data.iteritems():
            if not isinstance(_pdata, ParsedData):
                continue

            for _var, _val in _pdata.iteritems():
                if isinstance(_val, uilib.colors.Palette):
                    _list.append(_val.get_palette())

        return _list

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def attr(self, resolution, name):
        """
        Search for first matching attribute <name> according to resolution
        @return: Registered palette name
        """

        for _el in resolution:
            # Normalize name
            if not _el.startswith(u"ui."):
                _el = u"ui.%s" % _el

            if _el in self._data and (name in self._data[_el]):
                return self._data[_el][name].name

        # If none found return default
        return self._default.name
