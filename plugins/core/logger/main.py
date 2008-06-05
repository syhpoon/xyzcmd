#-*- coding: utf8 -*
#
# Author <e-mail> year
#

import libxyz.ui as uilib

from libxyz.ui import lowui
from libxyz.core.plugins import BasePlugin
from libxyz.core import Queue

from loglevel import LogLevel
from logentry import LogEntry

class XYZPlugin(BasePlugin):
    "Plugin logger"

    NAME = u"logger"
    AUTHOR = u"Max E. Kuznecov ~syhpoon <mek@mek.uz.ua>"
    VERSION = u"0.1"
    BRIEF_DESCRIPTION = u"Logger console"
    FULL_DESCRIPTION = u"Logger console is used to collect system messages.\n"\
                       u"There are several message levels:\n"\
                       u"ERROR: Critical error. Program must be closed.\n"\
                       u"WARNING: Non-critical warning.\n"\
                       u"INFO: Informational message.\n"\
                       u"DEBUG: Debug messages.\n"\
                       u"ALL: All of the above.\n"\
                       u"If no level specified log nothing."
    NAMESPACE = u"core"

    DOC = u"Plugin configuration:\n"\
          u"levels - a list of levels to track\n"\
          u"lines - max number of lines to be shown in logger console."

    _DEFAULT_LINES = 100

    def __init__(self, xyz):
        super(XYZPlugin, self).__init__(xyz)

        self.public = {u"show_console": self._show_console,
                       u"log": self._log,
                      }

        self._loglevel = LogLevel()

        self.public_data = {u"loglevel": self._loglevel}

        self._lines = self._DEFAULT_LINES
        self._level = self._loglevel.NONE

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def prepare(self):
        self._process_config()
        self._data = Queue(self._lines)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _show_console(self):
        """
        Show logger console
        """

        # Queue is actually subclassed from list, but SimpleListWalker
        # checks arg type by type(), not by isinstance()

        _walker = lowui.SimpleListWalker(list(self._data))

        _dim = tuple([x - 2 for x in self.xyz.screen.get_cols_rows()])

        uilib.XYZListBox(self.xyz, self.xyz.top, _walker,
                         _(u"Logger console"), _dim).show()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _log(self, msg, level=None):
        """
        Add new message to log

        @param msg: Message
        @param level: Log level
        @type level: L{LogLevel} attribute
        """

        if level is None:
            level = self._loglevel.UNKNOWN

        _attr = self.xyz.skin.attr(uilib.XYZListBox.resolution, u"selected")

        if self._level & level:
            self._data.append(LogEntry(msg, self._loglevel.str_level(level),
                              _attr))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _process_config(self):
        """
        See what variables are defined in plugins.conf, and set default if
        needed.
        """

        # Configuration for this plugin is not defined
        if self.ns.pfull not in self.xyz.conf[u"plugins"]:
            return

        try:
            self._lines = self.xyz.conf[u"plugins"][self.ns.pfull][u"lines"]
        except (KeyError, ValueError):
            pass

        try:
            self._level = self._calc_levels(
                            self.xyz.conf[u"plugins"][self.ns.pfull][u"levels"])
        except KeyError:
            pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _calc_levels(self, level_list):
        """
        Parse levels from config
        """

        _level = self._loglevel.NONE

        for _lvl in level_list:

            try:
                _level |= getattr(self._loglevel, _lvl)
            except KeyError:
                pass

        return _level
