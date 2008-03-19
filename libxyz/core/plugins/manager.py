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

import sys
import re
import os
import os.path

from libxyz.exceptions import PluginError, XYZValueError
from libxyz.parser import FlatParser

class PluginManager(object):
    """
    Plugin manager class
    It is supposed to:
    - Load found plugins
    - Provide easy access to plugin data
    """

    def __init__(self, xyz, dirs):
        """
        @param xyz: XYZ data
        @param dirs: Plugin directories list
        @type dirs: list
        """

        if type(dirs) != type([]):
            raise XYZValueError(_(u"Invalid argument type %s. List expected" %
                                  type(dirs)))
        else:
            self.dirs = dirs
            sys.path.extend(dirs)

        self.xyz = xyz

        self.abs_ns = "xyz:plugins:"

        self._loaded = {}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def load(self, plugin, *initargs, **initkwargs):
        """
        Load and initiate required plugin
        @param plugin: Absoulute or relative plugin namespace path
        @param initargs: Necessary arguments to initiate plugin
        @param initkwargs: Necessary kw arguments to initiate plugin
        """

        _plugin = self.normalize_ns_path(plugin)

        if self.is_loaded(_plugin):
            return self.get_loaded(_plugin)

        _path = u".".join((_plugin, u"main"))

        # Import plugin
        # Plugin entry-point is XYZPlugin class in a main.py file
        try:
            _loaded = __import__(_path, globals(), locals(), [u"XYZPlugin"])
        except ImportError, e:
            raise PluginError(_(u"Unable to load plugin %s: %s" % (plugin, e)))

        try:
            _loaded = getattr(_loaded, u"XYZPlugin")
        except AttributeError, e:
            raise PluginError(_(u"Unable to find required XYZPlugin class"))

        # Initiate plugin
        _obj = _loaded(self.xyz, *initargs, **initkwargs)

        # Run prepare (constructor)
        _obj.prepare()

        self.set_loaded(_plugin, _obj)

        return _obj

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def from_load(self, plugin, method):
        """
        Load method from plugin
        """

        _plugin = self.normalize_ns_path(plugin)

        if not self.is_loaded(_plugin):
            _obj = self.load(plugin)
        else:
            _obj = self.get_loaded(_plugin)

        if method not in _obj.public:
            raise PluginError(_(u"%s plugin instance does not export "\
                                u"%s method" % (plugin, method)))
        else:
            return _obj.public[method]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def is_loaded(self, plugin):
        """
        Check if plugin already loaded
        @param plugin: Normalized plugin path
        """

        return plugin in self._loaded

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_loaded(self, plugin):
        """
        Return loaded and initiated inistance of plugin
        @param plugin: Normalized plugin path
        """

        return self._loaded[plugin]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def set_loaded(self, plugin, inst):
        """
        Set loaded and initiated inistance of plugin
        @param plugin: Normalized plugin path
        @param inst: Plugin instance
        """

        self._loaded[plugin] = inst

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def normalize_ns_path(self, path):
        """
        Normalize plugin namespace path to relative.
        """

        _path = path

        if _path.startswith(self.abs_ns):
            _path = path.replace(self.abs_ns, u"")
        elif _path.startswith(u":"):
            _path = _path[1:]
        else:
            raise PluginError(_(u"Invalid plugin namespace path %s" % _path))

        return _path.replace(u":", u".")
