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

import libxyz.ui as uilib

from libxyz.ui import lowui
from libxyz.core.plugins import VirtualPlugin
from libxyz.core import Queue
from libxyz.core.logger.loglevel import LogLevel
from libxyz.core.logger.logentry import LogEntry

class Logger(object):
    """
    Logger console is used to collect system messages.
    There are several message levels:
    ERROR: Critical error.
    WARNING: Non-critical warning.
    INFO: Informational message.
    DEBUG: Debug messages.
    ALL: All of the above.
    """

    def __init__(self, xyz, levels, lines=100):
        """
        @param xyz: XYZ data
        @param levels: A list of levels to track
        @param lines: Max number of lines to be shown in logger console
        """

        self.xyz = xyz

        try:
            self.lines = int(lines)
        except ValueError:
            pass

        self.loglevel = LogLevel()
        self.tracked_levels = self._calc_levels(levels)

        self._lines = lines
        self._data = Queue(self._lines)

        self._set_internal_plugin()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def show_console(self):
        """
        Show logger console
        """

        # Queue is actually subclassed from list, but SimpleListWalker
        # checks arg type by type(), not by isinstance(), so cast explicitly
        _walker = lowui.SimpleListWalker(list(self._data))
        _walker.focus = len(_walker) - 1

        _dim = tuple([x - 2 for x in self.xyz.screen.get_cols_rows()])

        uilib.XYZListBox(self.xyz, self.xyz.top, _walker,
                         _(u"Logger console"), _dim).show()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def log(self, msg, level=None):
        """
        Add new message to log

        @param msg: Message
        @param level: Log level
        @type level: L{LogLevel} attribute
        """

        if level is None:
            level = self.loglevel.UNKNOWN

        _sel_attr = self.xyz.skin.attr(uilib.XYZListBox.resolution, u"selected")

        if self.tracked_levels & level:
            self._data.append(LogEntry(msg, self.loglevel.str_level(level),
                              _sel_attr))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def clear(self):
        """
        Clear log queue
        """

        self._data.clear()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _calc_levels(self, level_list):
        """
        Parse levels from config
        """

        _level = self.loglevel.NONE

        for _lvl in level_list:
            _level |= _lvl

        return _level

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _set_internal_plugin(self):
        """
        Set own virtual plugin
        """

        _logger_plugin = VirtualPlugin(self.xyz, u"logger")
        _logger_plugin.AUTHOR = u"Max E. Kuznecov <syhpoon@syhpoon.name>"
        _logger_plugin.VERSION = u"0.1"
        _logger_plugin.BRIEF_DESCRIPTION = u"Logger plugin"
        _logger_plugin.FULL_DESCRIPTION = re.sub(r"\ {2,}",
                                                 r"", self.__doc__).strip()
        _logger_plugin.HOMEPAGE = u"xyzcmd.syhpoon.name"

        _logger_plugin.export(self.show_console)
        _logger_plugin.export(self.log)
        _logger_plugin.export(self.clear)

        self.xyz.pm.register(_logger_plugin)
