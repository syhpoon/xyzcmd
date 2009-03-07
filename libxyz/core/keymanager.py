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

import re

import libxyz

from libxyz.core.plugins import Namespace
from libxyz.core.utils import ustring
from libxyz.exceptions import PluginError
from libxyz.exceptions import KeyManagerError
from libxyz.exceptions import XYZValueError
from libxyz.exceptions import LexerError

class KeyManager(object):
    """
    Key bindings management class
    """

    CONTEXT_DEFAULT = u"DEFAULT"
    CONTEXT_SELF = u"@"

    def __init__(self, xyz, confpathes):
        self.xyz = xyz
        self.confpathes = confpathes
        self.keys = libxyz.ui.Keys()

        self._loaded_methods = {}
        self._bind_data = {}
        self._args_data = {}

        self._path_sel = libxyz.PathSelector()

        self._parse_config()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def process(self, pressed, context=None):
        """
        Process pressed keys

        @return: Tuple (method, arguments)
        """

        context = context or self.CONTEXT_DEFAULT

        _p = tuple(pressed)

        _method = None
        _args = []

        # Look for binded shortcut
        try:
            _method = self._bind_data[context][_p]
        except KeyError:
            # No bind
            pass
        else:
            try:
                _args = self._args_data[context][_method]
            except KeyError:
                pass

        return (_method, _args)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _parse_config(self):
        def _comment_cb(mo):
            return

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def _load_cb(mo):
            try:
                self._load(mo.group("method"))
            except PluginError, e:
                raise XYZValueError(ustring(str(e)))

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def _bind_cb(mo):
            _method = mo.group("method")
            _shortcut = mo.group("shortcut")
            _context = mo.group("context")

            try:
                _args = _parse_args(mo.group("args"))
            except LexerError, e:
               raise XYZValueError(ustring(str(e)))

            if _context == self.CONTEXT_SELF:
                _context = Namespace(_method).pfull

            try:
                self._bind(_method, _shortcut, _context, _args)
            except KeyManagerError, e:
                raise XYZValueError(ustring(str(e)))

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def _parse_args(raw):
            _args = []

            if not raw:
                return _args

            _tokens = ("\n", ",")

            _lexer = libxyz.parser.Lexer(raw, _tokens,
                                         comment=None, macro=None)

            while True:
                _res = _lexer.lexer()
                
                if _res is None:
                    break
                else:
                    _args.append(_res[1])

            return filter(lambda x: x != u",", _args)
            
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        _comment_re = re.compile(r"^\s*#.*$")

        _include_re = re.compile(r"""
        ^                  # begin
        \s*                # leading spaces
        include            # keyword include
        \s+                # on or more spaces
        TODO
        $                  # EOL        
        """, re.VERBOSE)

        _load_re = re.compile(r"""
        ^                  # begin
        \s*                # leading spaces
        load               # keywoard load
        \s+                # one ore more spaces
        (?P<method>[\S:]+) # Full plugin path with method name
        \s*                # trailing spaces
        $                  # EOL
        """, re.VERBOSE)

        _bind_re = re.compile(r"""
        ^                   # begin
        \s*                 # leading spaces
        bind                # keywoard bind
        \s+                 # one ore more spaces
        (?P<method>[\w:]+)  # plugin method name
        \s*                 # spaces
        (\((?P<args>.*)\))? # arguments                
        \s+                 # one ore more spaces
        to                  # keyword to
        \s+                 # one ore more spaces
        (?P<shortcut>\S+)   # shortcut
        (                   # optional context group begin
        \s+                 # one ore more spaces
        context             # keyword context
        \s+                 # one ore more spaces
        (?P<context>[:\w_%s]+) # context name
        )?                  # context group end
        \s*                 # trailing spaces
        $                   # end
        """ % self.CONTEXT_SELF, re.VERBOSE)

        _cbpool = {_comment_re: _comment_cb,
                   _load_re: _load_cb,
                   _bind_re: _bind_cb,
                  }

        _parser = libxyz.parser.RegexpParser(_cbpool)

        # First mandatory system keys file

        try:
            _file = open(self.confpathes[0], "r")
        except IOError, e:
            raise XYZRuntimeError(_(u"Unable to open %s: %s" %
                                  (self.confpath, ustring(str(e)))))

        try:
            _parser.parse(_file)
        finally:
            _file.close()

        # Next optional user's keys file

        try:
            _file = open(self.confpathes[1], "r")
        except IOError, e:
            pass
        else:
            try:
                _parser.parse(_file)
            finally:
                _file.close()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _load(self, method):
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
        else:
            self._loaded_methods[_p.full] = self.xyz.pm.from_load(_p.pfull,
                                                                  _p.method)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _bind(self, method, shortcut, context=None, args=None):
        _p = Namespace(method)
        _mobj = None

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
            self.xyz.pm.wait_for(_p, self._bind_wait_cb, _p.method, shortcut,
                                 context, args)

        self.bind(_mobj, shortcut, context, args)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _bind_wait_cb(self, plugin_obj, method, shortcut, context, args):
        if method not in plugin_obj.public:
            xyzlog.error(_(u"Unable to bind method %s. "\
                         u"Plugin %s doesn't export it." %
                         (method, plugin_obj.ns.pfull)))
            return

        self.bind(plugin_obj.public[method], shortcut, context, args,
                  force=False)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def bind(self, mobj, shortcut, context=None, args=None, force=True):
        """
        Bind a shortcut to a method
        @return: True on success, False otherwise, also raises exception
                 if method was not loaded
        """

        _shortcut = self.keys.make_shortcut(shortcut)

        if context is None:
            context = self.CONTEXT_DEFAULT

        if context not in self._bind_data:
            self._bind_data[context] = {}

        if context not in self._args_data:
            self._args_data[context] = {}

        if _shortcut in self._bind_data[context] and \
        self._bind_data[context][_shortcut] is not None and not force:
            return

        self._bind_data[context][_shortcut] = mobj

        if args is None:
            args = []

        self._args_data[context][mobj] = args

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_binds(self):
        """
        Return keybindings data
        """

        return self._bind_data
