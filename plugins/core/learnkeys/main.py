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

import cPickle

import libxyz.ui as uilib

from libxyz.core.plugins import BasePlugin
from libxyz.core import UserData
from libxyz.exceptions import PluginError
from libxyz.exceptions import XYZRuntimeError

class XYZPlugin(BasePlugin):
    """
    Learn terminal keycodes
    """

    NAME = u"LearnKeys"
    AUTHOR = u"Max E. Kuznecov ~syhpoon <mek@mek.uz.ua>"
    VERSION = u"0.1"
    NAMESPACE = u"core"

    BRIEF_DESCRIPTION = u"Setup terminal keycodes"

    FULL_DESCRIPTION = u"LearnKeys plugin is used to properly "\
                       u"configure terminal keycodes."

    def __init__(self, xyz):
        super(XYZPlugin, self).__init__(xyz)

        self.public = {u"learn_keys": self._learn_keys_dialog}

        self._ud = UserData()

        self.keys = (("F1", uilib.Keys.F1),
                     ("F2", uilib.Keys.F2),
                     ("F3", uilib.Keys.F3),
                     ("F4", uilib.Keys.F4),
                     ("F5", uilib.Keys.F5),
                     ("F6", uilib.Keys.F6),
                     ("F7", uilib.Keys.F7),
                     ("F8", uilib.Keys.F8),
                     ("F9", uilib.Keys.F9),
                     ("F10", uilib.Keys.F10),
                     ("F11", uilib.Keys.F11),
                     ("F12", uilib.Keys.F12),
                     ("F13", uilib.Keys.F13),
                     ("F14", uilib.Keys.F14),
                     ("F15", uilib.Keys.F15),
                     ("F16", uilib.Keys.F16),
                     ("F17", uilib.Keys.F17),
                     ("F18", uilib.Keys.F18),
                     ("F19", uilib.Keys.F19),
                     ("F20", uilib.Keys.F20),
                     ("BACKSPACE", uilib.Keys.BACKSPACE),
                     ("END", uilib.Keys.END),
                     ("UP", uilib.Keys.UP),
                     ("DOWN", uilib.Keys.DOWN),
                     ("LEFT", uilib.Keys.LEFT),
                     ("RIGHT", uilib.Keys.RIGHT),
                     ("HOME", uilib.Keys.HOME),
                     ("PAGE UP", uilib.Keys.PAGE_UP),
                     ("PAGE DOWN", uilib.Keys.PAGE_DOWN),
                     ("INSERT", uilib.Keys.INSERT),
                     ("TAB", uilib.Keys.TAB),
                    )

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def prepare(self):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def finalize(self):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _learn_keys_dialog(self):
        """
        Show LearnKeys dialog
        """

        _title = _(u"%s - %s" % (self.NAME, self.VERSION))

        # TODO: добавить разделение по типу терминала {TERM: {}...}
        _pressed = self._load_data()

        for _label, _key in self.keys:
            _msg = _(u"Please press key %s\n"\
                     u"Press ENTER to skip key\n"\
                     u"Press ESCAPE to quit dialog" % _label)
            _p = uilib.MessageBox(self.xyz, self.xyz.top, _msg, _title).show()

            if _p == [] or _p[0] == uilib.Keys.ENTER:
                continue

            if _p[0] == uilib.Keys.ESCAPE:
                break

            if _p[0] != _key:
                _pressed[tuple(_p)] = _key

        _ask_msg = _(u"Save learned keys?")

        if uilib.YesNoBox(self.xyz, self.xyz.top, _ask_msg, _title).show():
            # Save data
            self._save_data(_pressed)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _save_data(self, data):
        """
        Store learned keycodes
        """

        try:
            _file = self._ud.openfile("keycodes", "wb", subdir="data")
        except XYZRuntimeError, e:
            raise PluginError(_(u"Unable to open file: %s" % unicode(e)))

        try:
            cPickle.dump(data, _file)
        except cPickle.PicklingError:
            raise PluginError(_(u"Unable to save learned data"))
        finally:
            _file.close()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def _load_data(self):
        """
        Load stored keycodes
        """

        _data = {}

        try:
            _file = self._ud.openfile("keycodes", "rb", subdir="data")
        except XYZRuntimeError, e:
            # Skip open error
            pass
        else:
            _data = cPickle.load(_file)
            _file.close()

        return _data
