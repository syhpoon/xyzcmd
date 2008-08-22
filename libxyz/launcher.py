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

"""
Launcher - all neccessary initialization
"""

import sys
import gettext
import getopt
import re
import os
import os.path

import libxyz
import libxyz.ui as uilib
import libxyz.const as const
import libxyz.parser as parser
import libxyz.core as core

from libxyz.ui import lowui
from libxyz.version import Version
from libxyz.core.plugins import PluginManager
from libxyz.core import logger

from libxyz.exceptions import XYZValueError
from libxyz.exceptions import XYZRuntimeError
from libxyz.exceptions import ParseError

class Launcher(object):
    """
    Startup class
    """

    def __init__(self):
        """
        Initialization
        """

        gettext.install(u"xyzcmd")

        self.cmdopts = "c:vh"
        self.xyz = core.XYZData()
        self.xyz.conf = {}

        self._path_sel = libxyz.PathSelector()
        self._conf_dir = None

        self._init_default()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _init_default(self):
        """
        Define some default values
        """

        self._conf_dir = const.CONF_DIR

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def run(self):
        """
        Run commander
        """

        self.parse_args()
        self.parse_configs()
        self.init_skin()

        self.xyz.pm = PluginManager(self.xyz, self._path_sel.get_plugins_dir())

        self.init_keys()

        self.init_logger()
        self.xyz.input = core.InputWrapper(self.xyz)
        self.xyz.screen = uilib.display.init_display()
        self.xyz.screen.register_palette(self.xyz.skin.get_palette_list())
        self.xyz.skin.set_screen(self.xyz.screen)
        self.xyz.screen.run_wrapper(self._run)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _run(self):
        _dim = self.xyz.screen.get_cols_rows()
        panel = uilib.Panel(self.xyz)
        self.xyz.top = lowui.Filler(panel)

        panel.loop()

        self.finalize()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def parse_args(self):
        """
        Parse command line arguments
        """

        try:
            _opts, _args = getopt.getopt(sys.argv[1:], self.cmdopts)
        except getopt.GetoptError, e:
            self.error(str(e))
            self.usage()
            self.quit()

        for _o, _a in _opts:
            if _c == "-c":
                self._conf_dir = _a
            elif _o == "-v":
                self.version()
                self.quit()
            else:
                self.usage()
                self.quit()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def init_logger(self):
        """
        Initiate Logger object and set it to builtin namespace
        """

        import __builtin__

        _log = logger.LogLevel()

        try:
            _levels = self.xyz.conf[u"plugins"][u":sys:logger"][u"levels"]
        except KeyError:
            _levels = (logger.LogLevel().ALL,)
        else:
            if not isinstance(_levels, tuple):
                _levels = (_levels,)

        try:
            _levels = [getattr(_log, x) for x in _levels]
        except Exception:
            raise XYZValueError(_(u"Invalid value %s.\n"\
                                  u"A list of valid log levels expected"
                                  % unicode(_levels)))

        try:
            _lines = self.xyz.conf[u"plugins"][u":sys:logger"][u"lines"]
        # Value not defined in conf
        except KeyError:
            _lines = 100

        try:
            _lines = abs(int(_lines))
        except ValueError:
            raise XYZValueError(_(u"Invalid value %s. "\
                                  u"A positive integer expected" %
                                  unicode(_lines)))

        _logger = core.logger.Logger(self.xyz, _levels, _lines)

        __builtin__.__dict__["xyzlog"] = _logger

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def init_skin(self):
        """
        Initialize skin
        """

        _system, _user = self._path_sel.get_skin(self.xyz.conf[u"xyz"][u"skin"])

        _path = self._path_sel.get_first_of((_user, _system))

        if _path is None:
            _path = self._path_sel.get_skin(const.DEFAULT_SKIN)[0]

        try:
            self.xyz.skin = core.Skin(_system)
        except SkinError, e:
            self.error(_(u"Unable to load skin file: %s" % e))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def init_keys(self):
        """
        Initialize keys
        """

        self.xyz.km = core.KeyManager(self.xyz,
                                  self._path_sel.get_conf(const.KEYS_CONF_FILE))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def parse_configs(self):
        """
        Parse configuration
        """

        self.xyz.conf[u"xyz"] = self._parse_conf_xyz()
        self.xyz.conf[u"plugins"] = self._parse_conf_plugins()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _parse_conf_xyz(self):
        """
        Parse main config
        """

        def _validate_plugins(block, var, val):
            if val == u"ENABLE":
                return True
            elif val == u"DISABLE":
                return False
            else:
                raise XYZValueError(_(u"Invalid value %s.\n"\
                                      u"Available values are: "\
                                      u"ENABLED, DISABLE" % val))

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def _validate_main(var, val):
            return val

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        _plugins_opts = {
                         u"count": 1,
                         u"varre": re.compile("^[\w:-]+$"),
                         u"assignchar": ">",
                         u"value_validator": _validate_plugins,
                        }
        _plugins_p = parser.BlockParser(_plugins_opts)

        _flat_vars = (u"skin", u"local_encoding")
        _flat_opts = {
                      u"count": 1,
                      u"assignchar": u"=",
                      u"validvars": _flat_vars,
                      u"value_validator": _validate_main,
                     }
        _flat_p = parser.FlatParser(_flat_opts)

        _parser = parser.MultiParser({})
        _parser.register(u"plugins", _plugins_p)
        _parser.register(_flat_vars, _flat_p)

        return self._parse_conf_file(const.XYZ_CONF_FILE, _parser)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _parse_conf_plugins(self):
        """
        Parse plugins config
        """

        _opts = {
                 u"varre": re.compile("^[\w:-]+$"),
                 u"assignchar": "=",
                }

        _parser = parser.BlockParser(_opts)

        return self._parse_conf_file(const.PLUGINS_CONF_FILE, _parser)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _parse_conf_file(self, conf_file, parser):
        """
        Parse configuration files
        @param conf_file: File to parse
        @pararam parser: Parser instance
        """

        _confs = self._path_sel.get_conf(conf_file)

        try:
            _file = open(_confs[0], "r")
        except IOError, e:
            self.error(_(u"Unable to open system configuration file: %s" % e))

        try:
            _data = parser.parse(_file)
        except ParseError, e:
            self.error(str(e))
        finally:
            _file.close()


        # Now try to parse users's conf, if exists
        try:
            _file = open(_confs[1], "r")
        except IOError, e:
            pass
        else:
            try:
                _data = parser.parse(_file, _data)
            except ParseError, e:
                self.error(str(e))
            finally:
                _file.close()

        return _data

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def usage(self):
        """
        Show usage
        """

        print _(u"""\
%s version %s
Usage: %s [-c dir][-vh]
    -c  -- Directory with configuration files
    -v  -- Show version
    -h  -- Show this help message\
""" % (const.PROG, Version.version, os.path.basename(sys.argv[0])))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def version(self):
        """
        Show version
        """

        print _(u"%s version %s" % (const.PROG, Version.version))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def quit(self):
        """
        Quit program
        """

        sys.exit()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def error(self, msg, quit=True):
        """
        Print error message and optionally quit
        """

        try:
            xyzlog.log(msg)
        except NameError:
            # Before logger initiated, print errors to stdout
            print msg

        if quit:
            self.quit()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def finalize(self):
        """
        Perform shutdown procedures
        """

        pass
