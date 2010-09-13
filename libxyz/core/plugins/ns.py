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

from libxyz.exceptions import XYZValueError

class Namespace(object):
    """
    Plugin namespace abstraction
    """

    # All wildcard
    ALL = u"*"

    def __init__(self, path):
        _path = path

        if not path.startswith(u":"):
            raise XYZValueError(_(u"Invalid plugin path: %s") % path)
        else:
            _path = path[1:]

        _raw = _path.split(u":")
        _len = len(_raw)

        if _len < 2 or _len > 3:
            raise XYZValueError(_(u"Invalid plugin path: %s") % path)

        # Full namespace path
        self.full = path
        # Full plugin path without method name
        self.pfull = ":".join(("", _raw[0], _raw[1]))
        # Namespace part
        self.ns = _raw[0]
        # Plugin name
        self.plugin = _raw[1]
        # Method name
        self.method = None

        # Internal representation
        self.internal = self._make_intern(self.full)

        if _len == 3:
            self.method = _raw[2]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def set_method(self, method):
        """
        Add method name to namespace
        """

        self.method = method
        self.full += u":%s" % method
        self.internal = self._make_intern(self.full)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _make_intern(self, full):
        return full.replace(u":", u".")[1:]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return self.full

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __repr__(self):
        return self.__str__()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def __unicode__(self):
        return self.__str__()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __cmp__(self, other):
        return cmp(self.full, other)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __len__(self):
        return len(self.full)
