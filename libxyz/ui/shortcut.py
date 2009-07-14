#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008-2009
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

from libxyz.core.utils import ustring
from libxyz.exceptions import XYZValueError

from libxyz.ui import Keys

class Shortcut(object):
    """
    Shortcut abstraction
    """

    def __init__(self, sc=None, raw=None):
        if (sc is raw is sc is None) or ((sc, raw) == (None, None)):
            raise XYZValueError(
                _(u"Only one of the arguments must be provided"))

        self._keys = Keys()

        if sc:
            self.sc = sc
            self.raw = self._parse_sc(sc)
        elif raw:
            self.raw = raw
            self.sc = self._parse_raw(raw)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __hash__(self):
        return self._hash(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def __eq__(self, other):
        return self._hash(self) == self._hash(other)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return "<Shortcut: %s>" % str(self.sc)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    __repr__ = __str__

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _hash(self, obj):
        return hash(tuple(obj.raw))
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _parse_sc(self, sc):
        """
        Parse shortcut into raw form
        @param sc: List of shortcuts as read from config file
        """

        _shortcut = []

        for s in sc:
            _tmp = []
            
            for _key in s.split("-"):
                try:
                    _tmp.append(getattr(self._keys, _key))
                except AttributeError:
                    _tmp.append(_key)

            _shortcut.append(u" ".join([ustring(x) for x in _tmp]))

        return _shortcut

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _parse_raw(self, raw):
        """
        Make shortcut from raw keys received
        """

        _raw = []

        for el in raw:
            _data = el
            
            if el in (u"page up", u"page down"):
                _data = self._keys.get_key(raw)
            elif len(el) > 1: # Shortcut
                _data = u"-".join([self._keys.get_key(x) or x
                                   for x in el.split(u" ")])
                
            _raw.append(_data)

        return _raw
