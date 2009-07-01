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
import locale
import os
import os.path
import __builtin__

import libxyz
import libxyz.ui as uilib
import libxyz.const as const
import libxyz.core as core

from libxyz.ui import lowui
from libxyz.version import Version
from libxyz.core.plugins import PluginManager
from libxyz.core import logger
from libxyz.core import dsl
from libxyz.core.utils import ustring

from libxyz.exceptions import *

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
        self.dsl = dsl.XYZ(self.xyz)

        self._path_sel = libxyz.PathSelector()
        self._conf_dir = None
        self._saved_term = None

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

        self._set_enc()

        self.parse_args()
        self.parse_configs()
        self.init_skin()

        self.xyz.term = core.utils.setup_term()
        self.xyz.hm = core.HookManager()
        self.xyz.pm = PluginManager(self.xyz,
                                    self._path_sel.get_plugins_dir())

        self.init_logger()
        self.init_actions()
        self.init_keys()

        self.xyz.input = core.InputWrapper(self.xyz)
        self.xyz.screen = uilib.display.init_display()
        self.xyz.screen.register_palette(self.xyz.skin.get_palette_list())
        self.xyz.skin.set_screen(self.xyz.screen)
        self.xyz.screen.run_wrapper(self._run)

        self.finalize()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _set_enc(self):
        """
        Try to preset local_encoding using current locale settings.
        After xyz conf is parsed, this value will be overriden by
        local_encoding from conf, if defined
        """

        __builtin__.__dict__["xyzenc"] = locale.getpreferredencoding()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _run(self):
        panel = uilib.Panel(self.xyz)
        self.xyz.top = lowui.Filler(panel)

        panel.loop()

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
            if _o == "-c":
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
        Initiate Logger object and put it into builtin namespace
        """

        _log = logger.LogLevel()

        try:
            _levels = self.xyz.conf[u"plugins"][u":sys:logger"][u"levels"]
        except KeyError:
            _levels = (logger.LogLevel().ALL,)
        else:
            if not isinstance(_levels, tuple) and not \
                   isinstance(_levels, list):
                _levels = (_levels,)

        try:
            _levels = [getattr(_log, x) for x in _levels]
        except Exception:
            raise XYZValueError(_(u"Invalid value %s.\n"\
                                  u"A list of valid log levels expected"
                                  % ustring(_levels)))

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
                                  ustring(_lines)))

        _logger = core.logger.Logger(self.xyz, _levels, _lines)

        __builtin__.__dict__["xyzlog"] = _logger

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def init_skin(self):
        """
        Initialize skin
        """

        _system, _user = self._path_sel.get_skin(
            self.xyz.conf[u"xyz"][u"skin"])

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
        Initialize keys manager
        """

        self.xyz.km = core.KeyManager(self.xyz, self._path_sel.get_conf(
                                                const.KEYS_CONF_FILE))
        self.xyz.km.parse_configs()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def init_actions(self):
        """
        Init action manager
        """

        self.xyz.am = core.ActionManager(self.xyz,
                                         self._path_sel.get_conf(
                                             const.ACTIONS_CONF_FILE))

        self.xyz.am.parse_configs()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def parse_configs(self):
        """
        Parse configuration
        """

        self._parse_conf_file(const.XYZ_CONF_FILE)
        self._parse_conf_file(const.PLUGINS_CONF_FILE)
        self._parse_conf_file(const.ALIASES_CONF_FILE)
        self._parse_conf_file(const.ICMD_CONF_FILE)

        # local_encoding set, override guessed encoding
        if u"local_encoding" in self.xyz.conf[u"xyz"]:
            __builtin__.__dict__["xyzenc"] = \
                                      self.xyz.conf[u"xyz"][u"local_encoding"]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _parse_conf_file(self, conf_file):
        """
        Parse configuration files, first system then user one if any
        @param conf_file: File to parse
        """

        _system, _user = self._path_sel.get_conf(conf_file)

        # Exec system config first
        try:
            dsl.exec_file(_system)
        except DSLError, e:
            self.error(_(u"Error parsing system config %s: %s") %
                       (_system, ustring(str(e))))

        # Now try to exec users's conf, if exists
        if os.path.exists(_user):
            try:
                dsl.exec_file(_user)
            except DSLError, e:
                self.error(_(u"Error parsing user config %s: %s") %
                           (_user, ustring(str(e))))

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

        if self.xyz.term is not None:
            core.utils.restore_term(self.xyz.term)
