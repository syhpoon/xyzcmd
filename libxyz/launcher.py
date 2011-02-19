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
import glob
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
from libxyz.core.utils import ustring, bstring
from libxyz.vfs import VFSDispatcher

from libxyz.exceptions import *

class Launcher(object):
    """
    Startup class
    """

    EVENT_STARTUP = u"event:startup"

    def __init__(self):
        """
        Initialization
        """

        self._path_sel = libxyz.PathSelector()
        gettext.install(u"xyzcmd", localedir=self._path_sel.get_locale_dir(),
                        unicode=True)

        self.cmdopts = "d:c:s:lvh"
        self._list_skins = False
        self.allowed_colors = (1, 16, 88, 256)

        self.xyz = core.XYZData()
        self.xyz.conf = {}
        self.xyz.hm = core.HookManager()
        self.dsl = dsl.XYZ(self.xyz)
        self.xyz.sm = core.SkinManager()
        self.xyz.am = core.ActionManager(self.xyz)
        self.xyz.km = core.KeyManager(self.xyz)
        self.xyz.vfs = VFSDispatcher(self.xyz)
        self.xyz.pm = PluginManager(self.xyz,
                                    self._path_sel.get_plugins_dir())

        self._conf = {}
        self._saved_term = None
        self._driver = None
        self._started = False

        self._create_home()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def run(self):
        """
        Run commander
        """

        self._set_enc()

        self.parse_args()
        self.parse_configs_1()

        if self._list_skins:
            self._show_skins()
            self.quit()

        self._driver = self._conf.get("driver",
                                      self.xyz.conf["xyz"]["term_lib"])

        self.xyz.term = core.utils.setup_term()

        self.init_logger()

        self.xyz.input = core.InputWrapper(self.xyz)
        self.xyz.screen = uilib.display.init_display(self._driver)
        self.xyz.driver = self._driver

        self.init_skin()
        self.parse_configs_2()

        self._started = True
        xyzlog.process_pending()

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

        self.xyz.hm.dispatch(self.EVENT_STARTUP)
        panel.loop()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _create_home(self):
        """
        Create .xyzcmd in homedir
        """

        if os.path.isdir(self._path_sel.user_dir):
            return

        try:
            os.makedirs(self._path_sel.user_dir)

            for d in (const.CONF_DIR,
                      const.PLUGINS_DIR,
                      const.SKINS_DIR,
                      ):
                os.mkdir(os.path.join(self._path_sel.user_dir, d))
        except Exception:
            return

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
            if _o == "-d":
                self._conf["driver"] = _a
            elif _o == "-c":
                _colors = int(_a)
                self._conf["colors"] = _colors
            elif _o == "-s":
                self._conf["skin"] = _a
            elif _o == "-l":
                self._list_skins = True
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
                                  u"A list of valid log levels expected")
                                  % ustring(_levels))

        try:
            _lines = self.xyz.conf[u"plugins"][u":sys:logger"][u"lines"]
        # Value not defined in conf
        except KeyError:
            _lines = 100

        try:
            _lines = abs(int(_lines))
        except ValueError:
            raise XYZValueError(_(u"Invalid value %s. "\
                                  u"A positive integer expected") %
                                  ustring(_lines))

        _logger = core.logger.Logger(self.xyz, _levels, _lines)

        __builtin__.__dict__["xyzlog"] = _logger

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def init_skin(self):
        """
        Init selected skin
        """

        colors = self._conf.get("colors",
                                self.xyz.conf["xyz"]["term_colors"])

        if colors not in self.allowed_colors:
            self.usage()
            self.quit()

        skin = self.xyz.sm.get(self._conf.get("skin",
                                              self.xyz.conf[u"xyz"][u"skin"]))


        if skin and skin.colors and colors not in skin.colors:
            xyzlog.warning(_(u"Skin %s is not usable with requested "\
                             u"color settings. Using default.") % skin.name)
            skin = self.xyz.sm.get(const.DEFAULT_SKIN)

        if skin is None:
            skin = self.xyz.sm.get(const.DEFAULT_SKIN)

        # Purge unused skins to save some memory
        self.xyz.sm.clear()

        self.xyz.screen.register_palette(skin.get_palette_list(self._driver))

        if hasattr(self.xyz.screen, "set_terminal_properties"):
            self.xyz.screen.set_terminal_properties(colors=colors)

        self.xyz.skin = skin
        self.xyz.skin.set_screen(self.xyz.screen)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def parse_configs_1(self):
        """
        Parse configuration. Phase 1
        """

        self._parse_conf_file(const.XYZ_CONF_FILE)
        self._parse_conf_file(const.PLUGINS_CONF_FILE)
        self._parse_conf_file(const.ALIASES_CONF_FILE)
        self._parse_conf_file(const.ICMD_CONF_FILE)
        self._parse_conf_file(const.VFS_CONF_FILE)
        self._parse_conf_file(const.HOOKS_CONF_FILE)

        # Load skins
        self._parse_skins()

        # local_encoding set, override guessed encoding
        if "local_encoding" in self.xyz.conf["xyz"]:
            __builtin__.__dict__["xyzenc"] = \
                                      self.xyz.conf["xyz"]["local_encoding"]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def parse_configs_2(self):
        """
        Parse configuration. Phase 2
        """

        self._parse_conf_file(const.KEYS_CONF_FILE)
        self._parse_conf_file(const.ACTIONS_CONF_FILE)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _parse_conf_file(self, conf_file):
        """
        Parse configuration files, first system then user one if any
        @param conf_file: File to parse
        """

        _system, _user = self._path_sel.get_conf(conf_file)

        # Exec system config first
        self._parse_file(_system, _(u"Error parsing system config %s: %s"))

        # Now try to exec users's conf, if exists
        if os.path.exists(_user):
            self._parse_file(_user, _(u"Error parsing user config %s: %s"))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _parse_skins(self):
        """
        Load all skins in system and user home dirs
        """

        user_skins, system_skins = self._path_sel.get_skins_dir()

        system_skins = glob.glob(os.path.join(system_skins, "*"))

        if os.path.exists(user_skins):
            user_skins = glob.glob(os.path.join(user_skins, "*"))
        else:
            user_skins = []

        for skin in system_skins + user_skins:
            res = self._parse_file(skin, error=False)

            if res != True:
                self.error(_(u"Skipping skin %s due to parsing error: %s") %
                           (skin, res), False)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _parse_file(self, file, tmpl=None, error=True):
        """
        Parse XYZCommander config
        """

        if tmpl is None:
            tmpl = _(u"Error parsing config %s: %s")

        try:
            dsl.exec_file(file)
        except DSLError, e:
            if error:
                self.error(tmpl % (file, unicode(e)))
            else:
                return unicode(e)

        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def usage(self):
        """
        Show usage
        """

        print _(u"""\
%s version %s
Usage: %s [-d driver][-c colors][-s skin][-lvh]
    -d  -- Display driver (raw (default) or curses)
    -c  -- Number of colors terminal supports (1, 16 (default), 88, 256)
    -s  -- Skin name
    -l  -- Show available skins
    -v  -- Show version
    -h  -- Show this help message\
""") % (const.PROG, Version.version, os.path.basename(sys.argv[0]))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def version(self):
        """
        Show version
        """

        print _(u"%s version %s") % (const.PROG, Version.version)

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

        if self._started:
            xyzlog.log(msg)
        else:
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

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _show_skins(self):
        """
        Show installed skins
        """

        for skin in self.xyz.sm.get_all():
            print "%s\t-- %s" % (skin.name, skin.version)
