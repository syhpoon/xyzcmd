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

from libxyz.exceptions import PluginError
from libxyz.exceptions import XYZValueError
from libxyz.core.plugins import BasePlugin
from libxyz.core.plugins import Namespace

def ns_transform(func):
    """
    Transform passed ns plugin path to libxyz.core.plugins.Namespace instance
    """

    def _trans(instance, *args, **kwargs):
        _path, _rest = args[0], args[1:]

        if not isinstance(_path, Namespace):
            _path = Namespace(_path)

        return func(instance, _path, *_rest, **kwargs)

    return _trans

#++++++++++++++++++++++++++++++++++++++++++++++++

class PluginManager(object):
    """
    Plugin manager class
    It is supposed to provide easy access to plugin data
    """

    PLUGIN_CLASS = u"XYZPlugin"
    VIRTUAL_NAMESPACE = u"sys"

    def __init__(self, xyz, dirs):
        """
        @param xyz: XYZ data
        @param dirs: Plugin directories list
        @type dirs: list
        """

        if not isinstance(dirs, list):
            raise XYZValueError(_(u"Invalid argument type %s. List expected" %
                                  type(dirs)))
        else:
            sys.path.extend(dirs)

        self.xyz = xyz

        self.enabled = self._enabled_list()
        # Do not load all the enabled plugin at once
        # Do it on demand
        self._loaded = {}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @ns_transform
    def load(self, plugin, *initargs, **initkwargs):
        """
        Load and initiate required plugin
        @param plugin: Plugin namespace path
        @param initargs: Necessary arguments to initiate plugin
        @param initkwargs: Necessary kw arguments to initiate plugin
        """

        virtual = self.is_virtual(plugin)

        if not virtual and plugin.pfull not in self.enabled:
            raise PluginError(_(u"Plugin %s is disabled or does not exists" %
                                plugin))

        if self.is_loaded(plugin):
            return self.get_loaded(plugin)

        if virtual:
            # If reached here, plugin is not loaded
            raise PluginError(_(u"Virtual plugin %s does not exist" % plugin))

        plugin.set_method(u"main")

        # Import plugin
        # Plugin entry-point is XYZPlugin class in a main.py file
        try:
            _loaded = __import__(plugin.internal, globals(), locals(),
                                [self.PLUGIN_CLASS])
        except ImportError, e:
            raise PluginError(_(u"Unable to load plugin %s: %s" % (plugin, e)))

        try:
            _loaded = getattr(_loaded, self.PLUGIN_CLASS)
        except AttributeError, e:
            raise PluginError(_(u"Unable to find required %s class" % \
                              self.PLUGIN_CLASS))

        # Initiate plugin
        _obj = _loaded(self.xyz, *initargs, **initkwargs)

        # Run prepare (constructor)
        _obj.prepare()

        self.set_loaded(plugin, _obj)

        return _obj

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @ns_transform
    def reload(self, plugin, *initargs, **initkwargs):
        """
        Force load plugin if it's already in cache.
        """

        if self.is_virtual(plugin):
            # Virtual plugins do not support reloading
            return None

        if self.is_loaded(plugin):
            self.del_loaded(plugin)

        return self.load(plugin, *initargs, **initkwargs)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @ns_transform
    def from_load(self, plugin, method):
        """
        Load method from plugin.
        If plugin was not loaded before, load and initiate it first.

        @param plugin: Plugin namespace path
        @param method: Public method name
        """

        if not self.is_loaded(plugin):
            _obj = self.load(plugin)
        else:
            _obj = self.get_loaded(plugin)

        if method not in _obj.public:
            raise PluginError(_(u"%s plugin instance does not export "\
                                u"method %s" % (plugin, method)))
        else:
            return _obj.public[method]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @ns_transform
    def is_loaded(self, plugin):
        """
        Check if plugin already loaded
        @param plugin: Plugin namespace path
        """

        return plugin.full in self._loaded

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @ns_transform
    def get_loaded(self, plugin=None):
        """
        Return loaded and initiated inistance of plugin
        @param plugin: Plugin namespace path
        """

        return self._loaded[plugin.pfull]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_all_loaded(self):
        """
        Return all currenty loaded plugins as dictionary with plugins ns path
        as keys and instances as values
        """

        return self._loaded

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @ns_transform
    def set_loaded(self, plugin, inst):
        """
        Set loaded and initiated inistance of plugin
        @param plugin: Plugin namespace path
        @param inst: Plugin instance
        """

        self._loaded[plugin.pfull] = inst

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @ns_transform
    def del_loaded(self, plugin):
        """
        Delete loaded instance from cache
        @param plugin: Plugin namespace path
        """

        try:
            self.shutdown(plugin.pfull)
            del(self._loaded[plugin.pfull])
        except KeyError:
            pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def shutdown(self, plugin=None):
        """
        Run destructors on specified or all loaded plugins
        """

        def _fin(p):
            try:
                self._loaded[p].finalize()
            except StandardError:
                pass

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        if plugin is not None:
            _fin(plugin)
        else:
            for plugin_name in self._loaded:
                _fin(plugin_name)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def register(self, obj):
        """
        Register new plugin.
        @param obj: libxyz.core.BasePlugin inherited instance
        """

        if not isinstance(obj, BasePlugin):
            raise XYZValueError(_(u"BasePlugin instance expected, got: %s" %
                                  type(obj)))

        self.set_loaded(obj.ns, obj)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def is_virtual(self, plugin):
        return plugin.ns == self.VIRTUAL_NAMESPACE

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _enabled_list(self):
        """
        Make list of enabled plugins
        """

        _data = self.xyz.conf[u"xyz"][u"plugins"]
        return [_pname for _pname in _data if _data[_pname]]
