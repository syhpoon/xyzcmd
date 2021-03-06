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

from UserDict import DictMixin

class ODict(DictMixin):
    """
    Ordered dictionary
    Provides dictionary-like access to parsed values
    Input order is kept
    """

    def __init__(self, name=None):
        self.name = name
        self._keys = []
        self._values = []

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def next(self):
        return self

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def iteritems(self):
        return ((_k, _v) for _k, _v in zip(self._keys, self._values))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def keys(self):
        return self._keys

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def values(self):
        return self._values

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return u"<ODict object: %s>" % unicode([(k, v)
                                                for k, v in self.iteritems()])

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __repr__(self):
        return self.__str__()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __getitem__(self, var):
        return self.lookup(var)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __setitem__(self, var, val):
        self.set(var, val)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __delitem__(self, var):
        try:
            _at = self._keys.index(var)
            del(self._keys[_at])
            del(self._values[_at])
        except ValueError:
            raise KeyError()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __contains__(self, key):
        return key in self._keys

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __iter__(self):
        return (_k for _k in self._keys)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get(self, var, default):
        """
        Lookup for var or return default
        """

        try:
            self.lookup(var)
        except KeyError:
            return default

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def index(self, index):
        """
        Lookup variable by index
        """

        if index >= len(self._values):
            raise AttributeError()
        else:
            return self._values[index]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def lookup(self, var):
        """
        Lookup for value of variable
        If variable does not exist raise KeyError
        """

        for _k, _v in zip(self._keys, self._values):
            if var == _k:
                return _v
        else:
            raise KeyError()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def set(self, var, val):
        """
        Set new value to variable
        """

        # Replace existing key
        try:
            _at = self._keys.index(var)
            self._keys[_at] = var
            self._values[_at] = val
        except ValueError:
            self._keys.append(var)
            self._values.append(val)
