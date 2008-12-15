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

class HookManager(object):
    """
    Hooks dispatcher
    """

    def __init__(self):
        self._data = {}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def register(self, hook, proc):
        """
        Register proc to be run upon hook event
        """

        if hook not in self._data:
            self._data[hook] = []

        if not callable(proc):
            xyzlog.log(_(u"HookManager: Callable argument expected"),
                       xyzlog.loglevel.ERROR)
            return False

        self._data[hook].append(proc)

        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def clear(self, hook):
        """
        Clear all data assosiated with hook
        """

        self._data[hook] = []

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def dispatch(self, hook, *args, **kwargs):
        """
        Sequentially run procedures registered with provided hook
        """

        # No callbacks registered
        if hook not in self._data or not self._data[hook]:
            return False

        for proc in self._data[hook]:
            try:
                proc(*args, **kwargs)
            except Exception, e:
                xyzlog.log(_(u"Error running callback procedure for hook %s") %
                           str(e).decode(xyzenc), xyzlog.loglevel.ERROR)
                return False

        return True
