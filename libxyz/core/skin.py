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

from libxyz.exceptions import SkinError
from fsrule import FSRule
from odict import ODict
from utils import ustring

from libxyz.ui.colors import Palette, Foreground, Background

class SkinManager(object):
    """
    Store and manage defined skins
    """

    def __init__(self):
        self._skins = {}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def add(self, skin):
        """
        Add new sking to storage
        """

        if not isinstance(skin, Skin):
            raise SkinError(_(u"Invalid skin argument: %s. "\
                              u"libxyz.core.Skin instance expected!"
                              % type(skin)))
        else:
            self._skins[skin.name] = skin

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get(self, name):
        """
        Get stored skin instance

        @return: Either Skin isntance or None if was not stored
        """

        return self._skins.get(name, None)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def clear(self):
        """
        Clear storage
        """

        self._skins = {}

#++++++++++++++++++++++++++++++++++++++++++++++++

class Skin(object):
    """
    Skin object. Provides simple interface to defined skin rulesets.
    """

    def __init__(self, name=None, author=None, version=None,
                 description=None, colors=None, rules=None):

        self.name = name
        self.author = author
        self.version = version
        self.description = description
        self.rules = self._make_rules(rules)
        self.colors = colors
        self.screen = None

        # Default fallback palette
        self._default = Palette("default", 
                                Foreground("DEFAULT"),
                                Background("DEFAULT"))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return u"<Skin object: %s>" % ustring(self.name)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __repr__(self):
        return self.__str__()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __getitem__(self, key):
        return self.rules[key]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def set_screen(self, screen):
        self.screen = screen

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _make_rules(self, raw_rules):
        """
        Internalize rules
        """

        rules = {}

        for block, rsets in raw_rules.iteritems():
            if block not in rules:
                rules[block] = ODict()

            for (resource, palette) in rsets:
                if isinstance(resource, FSRule):
                    var = resource.raw_rule
                else:
                    var = resource

                palette.name = self._make_name(block, var)

                rules[block][resource] = palette

        return rules
                
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _make_name(self, block, resource):
        return "%s@%s" % (resource, block)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_palette_list(self):
        """
        Return list of defined palettes.
        It is usually passed to register_palette() function
        """

        _list = [self._default.get_palette()]

        for _name, _block in self.rules.iteritems():
            for _var, _val in _block.iteritems():
                if isinstance(_val, Palette):
                    _list.append(_val.get_palette())

        return _list

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def attr(self, resolution, name, default=True):
        """
        Search for first matching attribute <name> according to resolution
        @param resolution: Sequence of ruleset names
        @param name: Attribute name
        @param default: If True, return default palette in case attr
                        is not found, otherwise return None
        @return: Registered palette name
        """

        return self.palette(resolution, name, default).name

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def palette(self, resolution, name, default=True):
        """
        Search for first matching palette <name> according to resolution
        """

        for _w in resolution:
            # Normalize name
            if not _w.startswith(u"ui."):
                _w = u"ui.%s" % _w

            try:
                return self.rules[_w][name]
            except KeyError:
                pass

        if default:
            return self._default
        else:
            return None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_palette(self, block, name):
        try:
            return self.rules[block][name].name
        except KeyError:
            return None
