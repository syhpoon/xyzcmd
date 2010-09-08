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

import os
import cPickle

import libxyz.ui as uilib

from libxyz.core.plugins import BasePlugin
from libxyz.core import UserData
from libxyz.core.utils import ustring
from libxyz.exceptions import PluginError
from libxyz.exceptions import XYZRuntimeError

class XYZPlugin(BasePlugin):
    """
    Terminal keycodes handling
    """

    NAME = u"keycodes"
    AUTHOR = u"Max E. Kuznecov ~syhpoon <syhpoon@syhpoon.name>"
    VERSION = u"0.1"
    NAMESPACE = u"core"

    BRIEF_DESCRIPTION = _(u"Setup terminal keycodes")

    FULL_DESCRIPTION = _(u"keycodes plugin is used to properly "\
                         u"configure terminal keycodes.\n"\
                         u"For each terminal type keycodes are stored "\
                         u"independently. Terminal type determined "\
                         u"by examining "\
                         u"TERM environment variable.")

    HOMEPAGE = u"xyzcmd.syhpoon.name"
    EVENTS = [(u"show",
               _(u"Fires upon showing dialog")),
              ]

    def __init__(self, xyz):
        super(XYZPlugin, self).__init__(xyz)

        self.export(self.learn_keys)
        self.export(self.delete_keys)
        self.export(self.get_keys)

        self._keysfile = "keycodes"
        self._keyssubdir = "data"
        self._terminal = None

        self._ud = UserData()

        self._keys = uilib.Keys()

        self.keys = (("F1", self._keys.F1),
                     ("F2", self._keys.F2),
                     ("F3", self._keys.F3),
                     ("F4", self._keys.F4),
                     ("F5", self._keys.F5),
                     ("F6", self._keys.F6),
                     ("F7", self._keys.F7),
                     ("F8", self._keys.F8),
                     ("F9", self._keys.F9),
                     ("F10", self._keys.F10),
                     ("F11", self._keys.F11),
                     ("F12", self._keys.F12),
                     ("F13", self._keys.F13),
                     ("F14", self._keys.F14),
                     ("F15", self._keys.F15),
                     ("F16", self._keys.F16),
                     ("F17", self._keys.F17),
                     ("F18", self._keys.F18),
                     ("F19", self._keys.F19),
                     ("F20", self._keys.F20),
                     ("BACKSPACE", self._keys.BACKSPACE),
                     ("END", self._keys.END),
                     ("UP", self._keys.UP),
                     ("DOWN", self._keys.DOWN),
                     ("LEFT", self._keys.LEFT),
                     ("RIGHT", self._keys.RIGHT),
                     ("HOME", self._keys.HOME),
                     ("PAGE UP", self._keys.PAGE_UP),
                     ("PAGE DOWN", self._keys.PAGE_DOWN),
                     ("INSERT", self._keys.INSERT),
                     ("TAB", self._keys.TAB),
                    )

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def prepare(self):
        self._terminal = os.getenv("TERM") or "DEFAULT"

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def learn_keys(self):
        """
        Show LearnKeys dialog
        """

        self.fire_event("show")
        _title = _(u"%s - %s" % (self.NAME, self.VERSION))

        _pressed = self._load_data()

        if self._terminal not in _pressed:
            _pressed[self._terminal] = {}

        _msg = _(u"Please press key %s\nPress ENTER to skip key\n"\
                 u"Press ESCAPE to quit dialog")

        for _label, _key in self.keys:
            _m = _msg % _label
            _p = uilib.MessageBox(self.xyz, self.xyz.top, _m, _title).show()

            if _p == [] or _p[0] == self._keys.ENTER:
                continue

            if _p[0] == self._keys.ESCAPE:
                break

            _cur = _pressed[self._terminal]
            _tkey = tuple(_p)

            if _p[0] != _key or (_tkey in _cur and tuple(_p[0]) !=_cur[_tkey]):
                _cur[_tkey] = _key

        _ask_msg = _(u"Save learned keys?")

        if uilib.YesNoBox(self.xyz, self.xyz.top, _ask_msg, _title).show():
            # Save data
            self._save_data(_pressed)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def delete_keys(self, all=False):
        """
        Delete learned keycodes data.
        If all is True, delete all saved data for all terminal types,
        otherwise delete only current terminal type data.
        """

        if all:
            try:
                self._ud.delfile(self._keysfile, self._keyssubdir)
            except XYZRuntimeError, e:
                pass
        else:
            _data = self._load_data()

            if self._terminal in _data:
                del _data[self._terminal]

            try:
                self._save_data(_data)
            except PluginError, e:
                pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_keys(self, all=False):
        """
        Return saved keycodes data as dictionary.
        If all is True, return all saved data for all terminal types,
        otherwise return only current terminal type data.
        """

        _data = self._load_data()

        if not all:
            try:
                _data = _data[self._terminal]
            except KeyError:
                _data = {}

        return _data

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _save_data(self, data):
        """
        Store learned keycodes
        """

        try:
            _file = self._ud.openfile(self._keysfile, "wb", self._keyssubdir)
        except XYZRuntimeError, e:
            raise PluginError(_(u"Unable to open file: %s" % unicode(e)))

        try:
            cPickle.dump(data, _file)
        except cPickle.PicklingError:
            _file.close()
            raise PluginError(_(u"Unable to save learned data"))
        else:
            _file.close()

        # Update inputwrapper data to make it available without restarting
        self.xyz.input.update(data[self._terminal])

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def _load_data(self):
        """
        Load stored keycodes
        """

        _data = {}

        try:
            _file = self._ud.openfile(self._keysfile, "rb", self._keyssubdir)
        except XYZRuntimeError, e:
            # Skip open error
            pass
        else:
            _data = cPickle.load(_file)
            _file.close()

        return _data
