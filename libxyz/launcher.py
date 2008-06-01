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
        self._exit = False

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

        _skin = self._path_sel.get_skin(self.xyz.conf[u"xyz"][u"skin"])

        # Skin specified in config not found, load default
        if not _skin:
            _skin = self._path_sel.get_skin(const.DEFAULT_SKIN)

        self.xyz.skin = core.Skin(_skin)
        self.xyz.pm = PluginManager(self.xyz, self._path_sel.get_plugins_dir())

        self._set_internal_plugin()

        self.xyz.km = core.KeyManager(self.xyz,
                                 self._path_sel.get_conf(const.KEYS_CONF_FILE))
        self.xyz.input = core.InputWrapper(self.xyz)

        self._bind_defaults()

        self.xyz.screen = uilib.display.init_display()
        self.xyz.screen.register_palette(self.xyz.skin.get_palette_list())
        self.xyz.screen.run_wrapper(self._run)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _run(self):
        _dim = self.xyz.screen.get_cols_rows()
        self.xyz.top = lowui.Filler(uilib.Panel(self.xyz))

        _logger = self.xyz.pm.load(u":core:logger")
        _logger.log(u"Message 1", _logger.loglevel.ERROR)
        _logger.log(u"Message 2", _logger.loglevel.WARNING)
        _logger.log(u"Message 3", _logger.loglevel.INFO)
        _logger.log(u"Message 3", _logger.loglevel.INFO)
        _logger.log(u"Message 3", _logger.loglevel.INFO)
        _logger.log(u"Message 3", _logger.loglevel.INFO)
        _logger.log(u"Message 3", _logger.loglevel.INFO)
        _logger.log(u"Message 3", _logger.loglevel.INFO)
        _logger.log(u"Message 3", _logger.loglevel.INFO)
        _logger.log(u"Message 3", _logger.loglevel.INFO)
        _logger.log(u"Message 3", _logger.loglevel.INFO)
        _logger.log(u"Message 3", _logger.loglevel.INFO)
        _logger.log(u"Message 3", _logger.loglevel.INFO)
        _logger.log(u"Message 3", _logger.loglevel.INFO)
        _logger.log(u"Message 3", _logger.loglevel.INFO)
        _logger.log(u"Message 3", _logger.loglevel.INFO)
        _logger.log(u"He had read somewhere that the Eskimos had over two hundred different words for snow, without which their conversation would probably have got very monotonous. So they would distinguish between thin snow and thick snow, light snow and heavy snow, sludgy snow, brittle snow, snow that came in flurries, snow that came in drifts, snow that came in on the bottom of your neighbour's boots all over your nice clean igloo floor, the snows of winter, the snows of spring, the snows you remember from your childhood that were so much better than any of your modern snow, fine snow, feathery snow, hill snow, valley snow, snow that falls in the morning, snow that falls at night, snow that falls all of a sudden just when you were going out fishing, and snow that despite all your efforts to train them, the huskies have pissed on.", _logger.loglevel.INFO)
        _logger.log(u"Message 5", _logger.loglevel.INFO)
        _logger.log(u"Message 6", _logger.loglevel.INFO)
        _logger.log(u"Message 7", _logger.loglevel.INFO)
        _logger.log(u"Message 8",)
        _logger.log(u"Message 9", _logger.loglevel.INFO)
        _logger.log(u"Message a", _logger.loglevel.INFO)
        _logger.log(u"Message b", _logger.loglevel.INFO)
        _logger.log(u"Message t", _logger.loglevel.INFO)
        _logger.log(u"Message r", _logger.loglevel.INFO)
        _logger.log(u"Message y", _logger.loglevel.INFO)
        _logger.log(u"Message z", _logger.loglevel.INFO)

        while True:
            if self._exit:
                break

            self.xyz.screen.draw_screen(_dim, self.xyz.top.render(_dim, True))

            _input = self.xyz.input.get()

            if _input:
                self.xyz.km.process(_input)

        self.finalize()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _set_internal_plugin(self):
        """
        Set own virtual plugin
        """

        _launcher_plugin = core.plugins.VirtualPlugin(self.xyz, u"launcher")
        _launcher_plugin.export(u"shutdown", self.shutdown)
        _launcher_plugin.VERSION = u"0.1"
        _launcher_plugin.BRIEF_DESCRIPTION = u"Launcher plugin"

        self.xyz.pm.register(_launcher_plugin)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _bind_defaults(self):
        """
        Bind default shortcuts
        User defined (if any) will override default values
        """

        self.xyz.km.bind(self.shutdown, uilib.Keys.F10)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def parse_args(self):
        """
        Parse command line arguments
        """

        try:
            _opts, _args = getopt.getopt(sys.argv[1:], self.cmdopts)
        except getopt.GetoptError, e:
            print str(e)
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

        def _validate(block, var, val):
            if val == u"ENABLE":
                return True
            elif val == u"DISABLE":
                return False
            else:
                raise XYZValueError(_(u"Invalid value %s.\n"\
                                      u"Available values are: "\
                                      u"ENABLED, DISABLE" % val))

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def _set_default(data):
            for _required in (
                              (u"skin", const.DEFAULT_SKIN),
                              (u"plugins", parser.ParsedData(u"plugins")),
                             ):
                if _required[0] not in data:
                    data[_required[0]] = _required[1]

            return data

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        _plugins_opts = {
                         u"count": 1,
                         u"varre": re.compile("^[\w:-]+$"),
                         u"assignchar": ">",
                         u"value_validator": _validate,
                        }
        _plugins_p = parser.BlockParser(_plugins_opts)

        _flat_vars = (u"skin",)
        _flat_opts = {
                      u"count": 1,
                      u"assignchar": u"=",
                      u"validvars": _flat_vars,
                     }
        _flat_p = parser.FlatParser(_flat_opts)

        _parser = parser.MultiParser({})
        _parser.register(u"plugins", _plugins_p)
        _parser.register(_flat_vars, _flat_p)

        _path = self._path_sel.get_conf(const.XYZ_CONF_FILE)

        try:
            _file = open(_path, "r")
        except IOError, e:
            self.error(_(u"Unable to open configuration file: %s" % e))

        try:
            _data = _parser.parse(_file)
        except ParseError, e:
            self.error(str(e))
        finally:
            _file.close()

        # Set default values if needed
        _data = _set_default(_data)

        return _data

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _parse_conf_plugins(self):
        """
        Parse plugins config
        """

        def _validate(block, var, val):
            if var == u"levels":
                try:
                    return [x.strip() for x in val.split(u",")]
                except Exception:
                    raise XYZValueError(_(u"Invalid value %s.\n"\
                                          u"A list of log levels expected"
                                          % val))
            elif var == u"lines":
                try:
                    return abs(int(val))
                except ValueError:
                    raise XYZValueError(_(u"Invalid value %s.\n"\
                                          u"A positive integer expected" % val))

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        _opts = {
                 u"varre": re.compile("^[\w:-]+$"),
                 u"assignchar": "=",
                 u"value_validator": _validate,
                }

        _valid = (u"levels", u"lines")
        _parser = parser.BlockParser(_opts)

        _path = self._path_sel.get_conf(const.PLUGINS_CONF_FILE)

        try:
            _file = open(_path, "r")
        except IOError, e:
            self.error(_(u"Unable to open configuration file: %s" % e))

        try:
            _data = _parser.parse(_file)
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

        print msg

        if quit:
            self.quit()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def shutdown(self):
        """
        Quit program
        """

        _q = _(u"Really quit %s?" % const.PROG)
        _title = const.PROG

        if uilib.YesNoBox(self.xyz, self.xyz.top, _q, _title).show():
            self._exit = True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def finalize(self):
        """
        Perform shutdown procedures
        """

        self.xyz.pm.shutdown()
