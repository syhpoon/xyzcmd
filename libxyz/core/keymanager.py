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

import libxyz

from libxyz.core.plugins import Namespace
from libxyz.core.utils import ustring
from libxyz.core.utils import is_func

from libxyz.ui import Shortcut

from libxyz.exceptions import PluginError
from libxyz.exceptions import KeyManagerError

class KeyManager(object):
    """
    Key bindings management class
    """

    CONTEXT_DEFAULT = u"DEFAULT"
    CONTEXT_SELF = u"@"

    def __init__(self, xyz):
        self.xyz = xyz
        self.keys = libxyz.ui.Keys()

        self._loaded_methods = {}
        self._bind_data = {}
        self._prefixes = []

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def process(self, pressed, context=None):
        """
        Process pressed keys

        @return: Tuple (method, arguments)
        """

        context = context or self.CONTEXT_DEFAULT
        _p = Shortcut(raw=pressed)

        # Got prefix key. Now wait for another keystroke and proceed
        if _p in self._prefixes:
            _aux = self.xyz.input.get()
            _p = Shortcut(raw=pressed + _aux)

        _method = None

        # Look for binded shortcut
        try:
            _method = self._bind_data[context][_p]
        except KeyError:
            # No bind
            pass

        return _method

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def set_prefix(self, shortcut):
        """
        Set prefix key
        """

        if not isinstance(shortcut, Shortcut):
            raise KeyManagerError(_(u"Invalid shortcut type: %s.") %
                                  ustring(type(shortcut)))

        if shortcut not in self._prefixes:
            self._prefixes.append(shortcut)
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    

    def load(self, method):
        """
        Load method
        """

        _p = Namespace(method)

        # Already loaded
        if _p.full in self._loaded_methods:
            return

        # Wildcard
        if _p.method == _p.ALL:
            self._loaded_methods[_p.full] = _p.ALL
        # Just load and instantiate plugin
        elif _p.method is None:
            self.xyz.pm.load(_p)
        else:
            self._loaded_methods[_p.full] = self.xyz.pm.from_load(_p.pfull,
                                                                  _p.method)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def bind(self, method, shortcut, context=None):
        """
        Bind a shortcut to a method.
        A method can be either a string, in that case it should denote the
        plugin method or it can be a function.
        
        @return: True on success, False otherwise, also raises exception
                 if method was not loaded
        """

        if isinstance(method, basestring):
            _p = Namespace(method)
            _mobj = None

            if context == self.CONTEXT_SELF:
                context = _p.pfull

            # First check if methods were loaded by wildcard ALL
            if _p.full not in self._loaded_methods:
                if "%s:%s" % (_p.pfull, _p.ALL) not in self._loaded_methods:
                    raise KeyManagerError(_(u"Method %s not loaded" % _p))

                # Else try to load specified method
                try:
                    _mobj = self.xyz.pm.from_load(_p.pfull, _p.method)
                except PluginError, e:
                    raise KeyManagerError(_(u"Load error: %s" % e))
            else:
                _mobj = self._loaded_methods[_p.full]

            if _mobj is None:
                # Wait until plugin method is available and then run callback
                self.xyz.pm.wait_for(_p, self._bind_wait_cb, _p.method,
                                     shortcut, context)

        elif is_func(method):
            _mobj = method
            _mobj.ns = _(u"<Internal function object>")
        else:
            raise KeyManagerError(_(u"Invalid method type: %s. "\
                                    u"Must be string or function") %
                                  type(method))

        self._bind(_mobj, shortcut, context)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _bind_wait_cb(self, plugin_obj, method, shortcut, context):
        if method not in plugin_obj.public:
            xyzlog.error(_(u"Unable to bind method %s. "\
                         u"Plugin %s doesn't export it." %
                         (method, plugin_obj.ns.pfull)))
            return

        self._bind(plugin_obj.public[method], shortcut, context, force=False)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _bind(self, mobj, shortcut, context=None, force=True):
        if context is None:
            context = self.CONTEXT_DEFAULT

        if context not in self._bind_data:
            self._bind_data[context] = {}

        if shortcut in self._bind_data[context] and \
        self._bind_data[context][shortcut] is not None and not force:
            return

        self._bind_data[context][shortcut] = mobj

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_binds(self):
        """
        Return keybindings data
        """

        return self._bind_data
