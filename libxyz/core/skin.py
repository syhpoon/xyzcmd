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

from libxyz.parser import BlockParser
from libxyz.parser import FlatParser

import libxyz.ui as uilib

class SkinManager(object):
    """
    Skin manager. Provides simple interface to defined skin rulesets.
    """

    def __init__(self, path):
        """
        @param path: Path to skin file
        """

        if not os.access(path, os.R_OK):
            self.path = DEFAULT_SKIN_PATH
        else:
            self.path = path

        def palette_validator(var, val):
            """
            Make urwid-compatible attributes tuple
            """

            def get_color(cl, val):
                try:
                    return getattr(cl, val)
                except AttributeError:
                    raise ValueError(_("Invalid atrribute definition: %s" % s))

            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            _fg = colors.Foreground.DEFAULT
            _bg = colors.Background.DEFAULT
            _ma = None

            _atrrs = [x.strip() for x in val.split(",")]

            _fg = get_color(colors.Foreground, _atrrs[0])

            if len(_atrrs) > 1:
                _bg = get_color(colors.Background, _atrrs[1])
            if len(_atrrs) > 2:
                _ma = tuple(
                      [get_color(color.Monochrome, x) for x in _atrrs[2:]]
                      )

            return colors.Palette(_fg, _bg, _ma)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def priority_validator(var, val):
            """
            Validator for priority values (int)
            """

            return int(val)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # Prepare parsers

        _fs_type_opt = {"count": 1,
                        "value_validator": palette_validator,
                        "validvars": ("file", "dir", "block", "char",
                                      "link", "fifo", "socket"),
                        }
        self._fs_type_p = BlockParser(_fs_type_opt)

        _fs_perm_opt = {"count": 1,
                        "value_validator": palette_validator,
                        "varre": re.compile("\+?\d{4}"),
                       }
        self._fs_perm_p = BlockParser(_fs_perm_opt)

        _fs_owner_opt = {"count": 1,
                         "value_validator": palette_validator,
                         "varre": re.compile("(\w+)?(:(\w+))?$"),
                         }
        self._fs_owner_p = BlockParser(_fs_owner_opt)

        _fs_regexp_opt = {"count": 1,
                         "value_validator": palette_validator,
                         "varre": re.compile(".+"),
                         }
        self._fs_regexp_p = BlockParser(_fs_regexp_opt)

        _fs_priority_opt = {"count": 1,
                            "value_validator": priority_validator,
                            "validvars": ("type", "perm", "regexp", "owner"),
        self._fs_priority_p = BlockParser(_fs_priority_opt)

        _ui_opt = {"count": 1,
                   "value_validator": palette_validator,
                   }
        self._ui_p = BlockParser(_ui_opt)

        _flat_opt = {"count": 1}
        self._flat_p = FlatParser(_flat_opt)

        _parsers = {"fs.type": self._fs_type_p,
                    "fs.perm": self._fs_perm_p,
                    "fs.owner": self._fs_owner_p,
                    "fs.regexp": self._fs_regexp_p,
                    "fs.priority": self._fs_priority_p,
                    re.compile("ui\.(\w)+"), self._ui_p,
                    ("AUTHOR", "VERSION", "DESCRIPTION"): self._flat_p,
                    }

        _multi_opt = {"tokens": (":",)}
        multi = MultiParser(_parsers, _multi_opt)

        self._data = multi.parse(src)
