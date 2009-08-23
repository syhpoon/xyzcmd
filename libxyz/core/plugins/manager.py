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

import sys

from libxyz.exceptions import PluginError
from libxyz.exceptions import XYZValueError
from libxyz.core.plugins import BasePlugin
from libxyz.core.plugins import Namespace
from libxyz.core.utils import ustring

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
    PLUGIN_FILE = u"main"
    VIRTUAL_NAMESPACE = u"sys"
    EVENT_INIT = u"plugin_init"
    EVENT_FROM_LOAD = u"plugin_from_load"
    EVENT_FROM_LOAD_DATA = u"plugin_from_load_data"
    EVENT_PREPARE = u"plugin_prepare"
    EVENT_FIN = u"plugin_fin"

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
        self._waiting = {}

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

        if plugin.pfull not in self.enabled:
            raise PluginError(_(u"Plugin %s is disabled or does not exist" %
                                plugin))

        if self.is_loaded(plugin):
            return self.get_loaded(plugin)

        if virtual:
            # Do not raise any error here, because virtual plugins may be
            # initiated at runtime after keys conf is parsed.
            return None

        plugin.set_method(self.PLUGIN_FILE)

        self.xyz.hm.dispatch(self.EVENT_INIT, plugin)
        
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
        self.xyz.hm.dispatch(self.EVENT_PREPARE, _obj)
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

        self.xyz.hm.dispatch(self.EVENT_FROM_LOAD, plugin, method)
        
        if not self.is_loaded(plugin):
            _obj = self.load(plugin)
        else:
            _obj = self.get_loaded(plugin)

        # Possible case for virtual plugins
        if _obj is None:
            return None

        if method not in _obj.public:
            raise PluginError(_(u"%s plugin instance does not export "\
                                u"method %s" % (plugin, method)))
        else:
            return _obj.public[method]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @ns_transform
    def from_load_data(self, plugin, obj):
        """
        Load data object from plugin.
        If plugin was not loaded before, load and initiate it first.

        @param plugin: Plugin namespace path
        @param obj: Public data object name
        """

        self.xyz.hm.dispatch(self.EVENT_FROM_LOAD_DATA, plugin, obj)
        
        if not self.is_loaded(plugin):
            _obj = self.load(plugin)
        else:
            _obj = self.get_loaded(plugin)

        if obj not in _obj.public_data:
            raise PluginError(_(u"%s plugin instance does not export "\
                                u"data object %s" % (plugin, obj)))
        else:
            return _obj.public_data[obj]

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

        # Check for pending waiting plugins
        if plugin.pfull in self._waiting:
            # Try to run callback
            for _cb, _args in self._waiting[plugin.pfull]:
                try:
                    _cb(inst, *_args)
                except Exception, e:
                    xyzlog.warning(_(u"Error in wait_for() callback: %s" %
                               ustring(str(e))))
            del(self._waiting[plugin.pfull])

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

    @ns_transform
    def wait_for(self, plugin, callback, *args):
        """
        Some virtual plugins are not available at the parsing time.
        This method is used to wait while plugin is loaded and then run
        callback.
        Arguments to callback: loaded plugin obj, and all optional *args passed
        """

        # WTF? already loaded? No need to wait
        if self.is_loaded(plugin):
            return callback(self.get_loaded(plugin), *args)

        # Initiate storage
        if plugin.pfull not in self._waiting:
            self._waiting[plugin.pfull] = []

        # Register for waiting
        self._waiting[plugin.pfull].append((callback, args))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def shutdown(self, plugin=None):
        """
        Run destructors on specified or all loaded plugins
        """

        def _fin(p):
            try:
                self._loaded[p].finalize()
            except Exception:
                pass

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        _plugins = self._loaded if self._loaded else [plugin]
        
        for plugin_name in self._loaded:
            self.xyz.hm.dispatch(self.EVENT_FIN, self._loaded[plugin_name])
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
