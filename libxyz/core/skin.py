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
            # TODO:
            self.path = DEFAULT_SKIN_PATH
        else:
            self.path = path

        self._data = {}

        # Default fallback palette
        self._default = uilib.colors.Palette("default",
                        uilib.colors.Foreground("DEFAULT"),
                        uilib.colors.Background("DEFAULT"),
                        uilib.colors.Monochrome("DEFAULT"))

        # 1. Parse
        self._data = self._parse()

        # 2. Order parsed data
        self._check()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return "<Skin object: %s>" % str(self.path)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __repr__(self):
        return __str__()

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
                raise XYZValueError(_("Invalid literal for number"))

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # Prepare parsers

        _fs_type_opt = {"count": 1,
                        "value_validator": palette_validator,
                        "validvars": ("file", "dir", "block", "char",
                                      "link", "fifo", "socket"),
                        }
        _fs_type_p = BlockParser(_fs_type_opt)

        _fs_perm_opt = {"count": 1,
                        "value_validator": palette_validator,
                        "varre": re.compile("\+?\d{4}"),
                       }
        _fs_perm_p = BlockParser(_fs_perm_opt)

        _fs_owner_opt = {"count": 1,
                         "value_validator": palette_validator,
                         "varre": re.compile("(\w+)?(:(\w+))?$"),
                         }
        _fs_owner_p = BlockParser(_fs_owner_opt)

        _fs_regexp_opt = {"count": 1,
                         "value_validator": palette_validator,
                         "varre": re.compile(".+"),
                         }
        _fs_regexp_p = BlockParser(_fs_regexp_opt)

        _fs_priority_opt = {"count": 1,
                            "value_validator": priority_validator,
                            "validvars": ("type", "perm", "regexp", "owner"),
                            }
        _fs_priority_p = BlockParser(_fs_priority_opt)

        _ui_opt = {"count": 1,
                   "value_validator": palette_validator,
                   }
        _ui_p = BlockParser(_ui_opt)

        _flat_opt = {"count": 1}
        _flat_p = FlatParser(_flat_opt)

        _parsers = {"fs.type": _fs_type_p,
                    "fs.perm": _fs_perm_p,
                    "fs.owner": _fs_owner_p,
                    "fs.regexp": _fs_regexp_p,
                    "fs.priority": _fs_priority_p,
                    re.compile("ui\.(\w)+"): _ui_p,
                    ("AUTHOR", "VERSION", "DESCRIPTION"): _flat_p,
                    }

        _multi_opt = {"tokens": (":",)}
        _multi_p = MultiParser(_parsers, _multi_opt)

        _skinfile = open(self.path, "r")

        try:
            _data = _multi_p.parse(_skinfile)
        except ParseError, e:
            raise SkinError(_("Error parsing skin file: %s" % str(e)))
        finally:
            _skinfile.close()

        return _data

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _make_name(self, block, resource):
        return "%s@%s" % (block, resource)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _check(self):
        for _required in ("AUTHOR", "DESCRIPTION", "VERSION"):
            if _required not in self._data:
                raise SkinError(_("Missing required variable: %s" % _required))

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
            if not _el.startswith("ui."):
                _el = "ui.%s" % _el

            if _el in self._data and (name in self._data[_el]):
                return self._data[_el][name].name

        # If none found return default
        return self._default.name
