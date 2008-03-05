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

from libxyz.exceptions import ParseError, SkinError
from libxyz.parser import BlockParser
from libxyz.parser import FlatParser
from libxyz.parser import MultiParser

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
            self.path = DEFAULT_SKIN_PATH
        else:
            self.path = path

        self.author = None
        self.version = None
        self.description = None

        self._default_palette = "default"

        # 1. Parse
        self._data = self._parse()

        # 2. Order parsed data
        self._order()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _parse(self):
        def palette_validator(block, var, val):
            """
            Make urwid-compatible attributes tuple
            """

            _fg = uilib.colors.Foreground("DEFAULT")
            _bg = uilib.colors.Background("DEFAULT")
            _ma = uilib.colors.Monochrome("DEFAULT")

            if type(val) in types.StringTypes:
                _val = (val,)
            else:
                _val = [x.strip() for x in val]

            _fg = uilib.colors.Foreground(_val[0])

            if len(_val) > 1:
                _bg = uilib.colors.Background(_val[1])
            if len(_val) > 2:
                _ma = tuple([color.Monochrome(x) for x in _val[2:]])

            return uilib.colors.Palette(self._make_name(block, var), _fg, _bg,
                                        _ma)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def priority_validator(block, var, val):
            """
            Validator for priority values (int)
            """

            try:
                return int(val)
            except ValueError, e:
                raise XYZValueError(_("Invalid literal"))

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

    def _order(self):
        try:
            self.author = self._data["AUTHOR"]
            self.description = self._data["DESCRIPTION"]
            self.version = self._data["VERSION"]
        except KeyError, e:
            raise SkinError(_("Missing required variable: %s" % str(e)))
        else:
            del(self._data["AUTHOR"])
            del(self._data["DESCRIPTION"])
            del(self._data["VERSION"])

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_palette_list(self):
        """
        Return list of defined palettes.
        It is usually passed to register_palette() function
        """

        _list = []

        for _name, _pdata in self._data.iteritems():
            for _var, _val in _pdata.iteritems():
                if isinstance(_val, uilib.colors.Palette):
                    _list.append(_val.get_palette())

        return _list

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    
    def find(self, resolution, name):
        """
        Search for first matching palette according to resolution
        @return: Registered palette name in format name@block
        """

        for _el in resolution:
            if _el in self._data and name in self._data[_el]:
                return self._make_name(el, self._data[_el].name)

        # If none found return default
        return self._default_palette
