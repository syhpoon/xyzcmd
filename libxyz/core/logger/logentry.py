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

import time

import libxyz.ui as uilib
from libxyz.ui import lowui

class LogEntry(uilib.ListEntry):
    """
    Log message entry
    """

    def __init__(self, msg, level, selected_attr, entry_attr=None,
                 write_time=True):
        """
        @param msg: Message
        @param level: Log level
        @param selected_attr: Atrribute of selected entry
        @param entry_attr: Entry text attribute
        @param write_time: Whether to write timestamp in entry
        """

        super(LogEntry, self).__init__(msg, selected_attr, entry_attr)

        self.level = level

        if write_time:
            _time_clause = u"[%s]: " % time.strftime(r"%F %H:%M")
        else:
            _time_clause = ""

        self._text = u"%(_time_clause)s(%(level)s) %(msg)s" % locals()
        self._sel_attr = selected_attr
        self._entry_attr = entry_attr
        self._content = lowui.Text(self._text)
