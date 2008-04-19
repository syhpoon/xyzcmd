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

import re

import libxyz

from libxyz import exceptions

class KeyManager(object):
    """
    Key bindings management class
    """

    def __init__(self, xyz, confpath):
        self.xyz = xyz
        self.confpath = confpath

        self._loaded_plugins = {}
        self._path_sel = libxyz.PathSelector()

        self._parse_config()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _parse_config(self):
        def _comment_cb(mo):
            return

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def _from_cb(mo):
            _plugin = mo.group("plugin")
            _method = mo.group("method")
            self._from_load(_plugin, _method)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def _load_cb(mo):
            self._load_plugin(mo.group("plugin"))

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def _bind_cb(mo):
            _force = False
            if mo.group("force") == "!":
                _force = True

            _method = mo.group("method")
            _shortcut = mo.group("shortcut")
            _context = mo.group("context")

            self._bind(_method, _shortcut, _context, force=_force)
            return True

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        _comment_re = re.compile("^\s*#.*$")

        _from_re = re.compile("""
        ^                  # begin
        \s*                # leading spaces
        from               # keyword from
        \s+                # one ore more spaces
        (?P<plugin>[\w:]+) # plugin ns-path
        \s+                # one ore more spaces
        load               # keywoard load
        \s+                # one ore more spaces
        (?P<method>\w+)    # method name
        \s*                # trailing spaces
        $                  # EOL
        """, re.VERBOSE)

        _load_re = re.compile("""
        ^                  # begin
        \s*                # leading spaces
        load               # keywoard load
        \s+                # one ore more spaces
        (?P<plugin>[\w:]+) # plugin name
        \s*                # trailing spaces
        $                  # EOL
        """, re.VERBOSE)

        _bind_re = re.compile("""
        ^                   # begin
        \s*                 # leading spaces
        bind                # keywoard bind
        (?P<force>\!?)      # Optional ! (force) mark
        \s+                 # one ore more spaces
        (?P<method>[\w:]+)  # plugin ns-path and/or method name
        \s+                 # one ore more spaces
        to                  # keyword to
        \s+                 # one ore more spaces
        (?P<shortcut>\S+)   # shortcut
        (                   # optional context group begin
        \s+                 # one ore more spaces
        context             # keyword context
        \s+                 # one ore more spaces
        (?P<context>[\w_]+) # context name
        )?                  # context group end
        \s*                 # trailing spaces
        $                   # end
        """, re.VERBOSE)

        _cbpool = {_comment_re: _comment_cb,
                   _from_re: _from_cb,
                   _load_re: _load_cb,
                   _bind_re: _bind_cb,
                  }

        _parser = libxyz.parser.RegexpParser(_cbpool)
        try:
            _file = open(self.confpath, "r")
        except IOError, e:
            raise XYZRuntimeError(_(u"Unable to open %s: %s" %
                                  (self.confpath, unicode(e))))

        try:
            _parser.parse(_file)
        finally:
            _file.close()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _load_plugin(self, plugin):
        """
        Load plugin
        """

        # Already loaded
        if plugin in self._loaded_plugins:
            return

        _plugin = self.xyz.pm.load(plugin)

        self._loaded_plugins[plugin] = _plugin

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _from_load(self, plugin, method):
        """
        Load a method from plugin
        """

        if method in self._loaded_methods:
            return

        _method = self.xyz.pm.from_load(plugin, method)

        self._loaded_methods[method] = _method

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _bind(self, method, shortcut, context, force=False):
        """
        Bind a method to shortcut
        """

        _shortcut = Shortcut(shortcut)

        if _shortcut in self._bind_data and not force:
            return

        # Try by method name
        if method in self._loaded_methods:
            self._bind_data[Shortcut(shortcut)] = self._loaded_methods[method]
            return
