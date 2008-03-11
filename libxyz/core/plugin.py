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

from libxyz.exceptions import PluginError

class BasePlugin(object):
    """
    Parent class for all xyz-plugins
    """

    def __init__(self, name, meta, *args, **kwargs):
        """
        @param name: Plugin name
        @type name: string
        """

        self.name = name
        self.version = version[0]
        self.intversion = version[1]
        self.author = author
        self.bdescription = bdescription
        self.description = description

        # List of exported public methods
        self.public = {}

        self._name_internal = self.__class__.__name__

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def add_method(self, method):
        """
        Add method to public
        """

        if not callable(method):
            raise PluginError(_(u"Callable method required"))

        self.public[self._build_key(method)] = method

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def remove_method(self, name):
        """
        Remove method from public
        """

        try:
            del self.public[self._build_key(method)]
        except KeyError:
            pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _build_key(self, method):
        """
        Build full ierarchical method path
        """

        return ".".join((u"xyz", self._name_internal, method.__name__))
