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

import traceback

from libxyz.core.utils import ustring

class HookManager(object):
    """
    Hooks dispatcher
    """

    def __init__(self):
        self._data = {}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def register(self, event, proc):
        """
        Register proc to be run upon event occured
        """

        if event not in self._data:
            self._data[event] = []

        if not callable(proc):
            xyzlog.error(_(u"HookManager: Callable argument expected"))
            return False

        self._data[event].append(proc)

        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def clear(self, event):
        """
        Clear all data assosiated with an event
        """

        self._data[event] = []

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def dispatch(self, event, *args):
        """
        Sequentially run procedures registered with provided event
        """

        # No callbacks registered
        if event not in self._data or not self._data[event]:
            return False

        for proc in self._data[event]:
            try:
                proc(*args)
            except Exception, e:
                xyzlog.error(
                    _(u"Error running callback procedure for event %s") %
                    ustring(str(e)))

                xyzlog.debug(ustring(traceback.format_exc()))

                return False

        return True
