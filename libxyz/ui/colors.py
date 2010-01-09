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

import copy
import re

from libxyz.ui import lowui
from libxyz.exceptions import XYZValueError
from libxyz.ui.display import is_lowui_ge_0_9_9

class Color(object):
    """
    Base color
    """

    colors = {}
    ctype = u"base"

    def __init__(self, color):
        if not self.is_color_valid(color):
            raise XYZValueError(_(u"Invalid %s color: %s" % \
                                  (self.ctype, str(color))))

        self.color = None
        self._set_color(color)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def is_color_valid(self, color):
        """
        Check if color is valid
        """
        
        return color in self.colors

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _set_color(self, color):
        self.color = self.colors[color]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return u"<%s color: %s>" % (self.ctype, str(self.color))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __repr__(self):
        return self.__str__()

#++++++++++++++++++++++++++++++++++++++++++++++++

class Foreground(Color):
    """
    Foreground color
    """

    colors = {
              u"BLACK": u"black",
              u"BROWN": u"brown",
              u"YELLOW": u"yellow",
              u"WHITE": u"white",
              u"DEFAULT": u"default",

              u"DARK_BLUE": u"dark blue",
              u"DARK_MAGENTA": u"dark magenta",
              u"DARK_CYAN": u"dark cyan",
              u"DARK_RED": u"dark red",
              u"DARK_GREEN": u"dark green",
              u"DARK_GRAY": u"dark gray",

              u"LIGHT_GRAY": u"light gray",
              u"LIGHT_RED": u"light red",
              u"LIGHT_GREEN": u"light green",
              u"LIGHT_BLUE": u"light blue",
              u"LIGHT_MAGENTA": u"light magenta",
              u"LIGHT_CYAN": u"light cyan",
              }

    ctype = u"foreground"

#++++++++++++++++++++++++++++++++++++++++++++++++

class Background(Color):
    """
    Background color
    """

    colors = {
              u"BLACK": u"black",
              u"BROWN": u"brown",
              u"DEFAULT": u"default",

              u"DARK_RED": u"dark red",
              u"DARK_GREEN": u"dark green",
              u"DARK_BLUE": u"dark blue",
              u"DARK_MAGENTA": u"dark magenta",
              u"DARK_CYAN": u"dark cyan",

              u"LIGHT_GRAY": u"light gray",
              }

    ctype = u"background"

#++++++++++++++++++++++++++++++++++++++++++++++++

class Attribute(Color):
    """
    Terminal attributes
    """

    colors = {
        u"BOLD": u"bold",
        u"UNDERLINE": u"underline",
        u"BLINK": u"blink",
        u"STANDOUT": u"standout",
        }

    ctype = u"attribute"

#++++++++++++++++++++++++++++++++++++++++++++++++

class BaseHighColor(Color):
    """
    High color can contain value of form:
    
    #009 (0% red, 0% green, 60% red, like HTML colors)
    #fcc (100% red, 80% green, 80% blue)
    g40 (40% gray, decimal), 'g#cc' (80% gray, hex),
    #000, 'g0', 'g#00' (black),
    #fff, 'g100', 'g#ff' (white)
    h8 (color number 8), 'h255' (color number 255)
    """

    def is_color_valid(self, color):
        # Regular color is also valid
        if color in self.colors:
            return True

        # Else check for high color
        hexre = r"(?:\d|[a-fA-F])"
        hicolorre = re.compile(r"^((?:#%(hexre)s{3})|(?:g\d{1,3})|"\
                               r"(?:g#%(hexre)s{1,2})|(?:h\d{1,3}))$" %
                               locals())

        if hicolorre.match(color) is None:
            return False
        else:
            return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def _set_color(self, color):
        self.color = color

#++++++++++++++++++++++++++++++++++++++++++++++++

class ForegroundHigh(BaseHighColor):
    colors = Foreground.colors

#++++++++++++++++++++++++++++++++++++++++++++++++

class BackgroundHigh(BaseHighColor):
    colors = Background.colors

#++++++++++++++++++++++++++++++++++++++++++++++++

class Palette(object):
    """
    Palette abstraction
    """

    @classmethod
    def convert(cls, config):
        """
        Convert config text colors to tuple of instances
        """
        
        fg = config.get("foreground", None)

        if fg is not None:
            fg = Foreground(fg)

        bg = config.get("background", None)

        if bg is not None:
            bg = Background(bg)
            
        fg_attrs = [Attribute(x) for x in
                    config.get("fg_attributes", [])] or None
            
        mono = [Attribute(x) for x in config.get("mono", [])] or None

        fg_high = config.get("foreground_high", None)

        if fg_high is not None:
            fg_high = ForegroundHigh(fg_high)

        bg_high = config.get("background_high", None)

        if bg_high is not None:
            bg_high = BackgroundHigh(bg_high)

        return (fg, bg, fg_attrs, mono, fg_high, bg_high)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def __init__(self, name, fg, bg, fg_attrs=None, mono=None,
                 fg_high=None, bg_high=None):
        """
        Init palette.

        @param name: Palette name
        """

        self.name = name

        self._fg = None
        self._bg = None
        self._fg_attrs = None
        self._mono = None
        self._fg_high = None
        self._bg_high = None

        self.fg = fg
        self.bg = bg
        self.fg_attrs = fg_attrs
        self.mono = mono
        self.fg_high = fg_high
        self.bg_high = bg_high

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _fg_get(self):
        return self._fg

    def _fg_set(self, fg):
        if fg is not None and not isinstance(fg, Foreground):
            raise XYZValueError(_(u"Invalid argument type %s, "\
                                  u"libxyz.ui.color.Foreground instance "\
                                  u"expected." % type(fg)))
        else:
            self._fg = fg

    fg = property(_fg_get, _fg_set)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _bg_get(self):
        return self._bg

    def _bg_set(self, bg):
        if bg is not None and not isinstance(bg, Background):
            raise XYZValueError(_(u"Invalid argument type %s, "\
                                  u"libxyz.ui.color.Background or instance "\
                                  u"expected." % type(bg)))

        self._bg = bg

    bg = property(_bg_get, _bg_set)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _fg_attrs_get(self):
        return self._fg_attrs

    def _fg_attrs_set(self, attrs):
        if attrs is not None:
            for attr in attrs:
                if not isinstance(attr, Attribute):
                    raise XYZValueError(_(u"Invalid argument type %s, "\
                                          u"libxyz.ui.color.Attribute "\
                                          u"instance expected." % type(attr)))

        self._fg_attrs = attrs

    fg_attrs = property(_fg_attrs_get, _fg_attrs_set)
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _mono_get(self):
        return self._mono

    def _mono_set(self, mono):
        if mono is not None:
            for attr in mono:
                if not isinstance(attr, Attribute):
                    raise XYZValueError(_(u"Invalid argument type %s, "\
                                          u"libxyz.ui.color.Attribute "\
                                          u"instance expected." % type(mono)))

        self._mono = mono

    mono = property(_mono_get, _mono_set)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _fg_high_get(self):
        return self._fg_high

    def _fg_high_set(self, fg_high):
        if fg_high is not None and not isinstance(fg_high, ForegroundHigh):
            raise XYZValueError(_(u"Invalid argument type %s, "\
                                  u"libxyz.ui.color.ForegroundHigh instance "\
                                  u"expected." % type(fg_high)))
        else:
            self._fg_high = fg_high

    fg_high = property(_fg_high_get, _fg_high_set)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _bg_high_get(self):
        return self._bg_high

    def _bg_high_set(self, bg_high):
        if bg_high is not None and not isinstance(bg_high, BackgroundHigh):
            raise XYZValueError(_(u"Invalid argument type %s, "\
                                  u"libxyz.ui.color.BackgroundHigh instance "\
                                  u"expected." % type(bg_high)))
        else:
            self._bg_high = bg_high

    bg_high = property(_bg_high_get, _bg_high_set)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_palette(self):
        """
        Return urwid-compatible palette tuple
        """

        fg = self.fg.color
        fg_attrs = self.fg_attrs

        # Append attributes to foreground color
        if fg_attrs is not None:
            fg = ",".join([fg] + [x.color for x in fg_attrs])

        bg = self.bg.color
        mono = self.mono
        
        if mono is not None:
            mono = ",".join([x.color for x in mono])

        fg_high = self.fg_high

        if fg_high is not None:
            fg_high = fg_high.color
            
            if fg_attrs is not None:
                fg_high = ",".join([fg_high] + [x.color for x in fg_attrs])

        bg_high = self.bg_high

        if bg_high is not None:
            bg_high = bg_high.color

        result = (self.name, fg, bg, mono)

        if is_lowui_ge_0_9_9():
            result += (fg_high, bg_high)

        return result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def set_fg(self, fg):
        """
        Set foreground color
        """

        self.fg = fg

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def set_bg(self, bg):
        """
        Set background color
        """

        self.bg = bg

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def copy(self):
        """
        Return copy of Palette instance
        """

        return copy.deepcopy(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __call__(self, config):
        new = self.copy()
        
        fg, bg, fg_attrs, mono, fg_high, bg_high = self.convert(config)

        if fg:
            new.fg = fg
        if bg:
            new.bg = bg
        if fg_attrs:
            new.fg_attrs = fg_attrs
        if mono:
            new.mono = mono
        if fg_high:
            new.fg_high = fg_high
        if bg_high:
            new.bg_high = bg_high

        return new
