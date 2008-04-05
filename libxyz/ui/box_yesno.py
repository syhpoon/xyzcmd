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

from libxyz.ui import lowui
from libxyz.ui import align
from libxyz.ui import Box
from libxyz.ui import Border

import libxyz.ui

class YesNoBox(Box):
    """
    Yes/No box. Shows a message and waits for Yes or No button pressed
    """

    # Skin rulesets resolution order
    resolution = (u"yesno_box", u"box", u"widget")

    def __init__(self, xyz, body, message, title="", width=60):
        """
        @param xyz: XYZ dictionary
        @param body: Top-level widget
        @param message: Message to display
        @param title: Box title
        @param width: Box width (including mount box)

        Required resources: title, box, border, mount, button
        """

        super(YesNoBox, self).__init__(xyz, body, message, title, width)
        self.calc_size(6)

        self.keys = libxyz.ui.Keys()

        self._yes_txt = _(u"Yes")
        self._no_txt = _(u"No")
        self._value = False

        self._buttons = self._init_buttons()

        _title = self._strip_title(title.replace(u"\n", u" "))
        _title = lowui.Text(_title, align.CENTER)
        _title = lowui.AttrWrap(_title, self._attr(u"title"))

        _mount = lowui.AttrWrap(lowui.Filler(lowui.Text(u"")),
                                self._attr(u"mount"))

        # Main dialog text
        _text = lowui.Text((self._attr(u"box"), message), align.CENTER)
        _blank = lowui.Text((self._attr(u"box"), ""))

        _widgets = [_text, _blank, self._buttons]
        _box = lowui.Filler(lowui.Pile(_widgets), valign=align.BOTTOM)
        _box = Border(_box, _title, self._attr(u"border"))
        _box = lowui.AttrWrap(_box, self._attr(u"box"))

        _mount = lowui.Overlay(_mount, body, align.CENTER, self.full_width,
                             align.MIDDLE, self.full_height)
        _box = lowui.Overlay(_box, _mount, align.CENTER, self.box_width,
                             align.MIDDLE, self.box_height)

        self.parent_init(_box)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def show(self, dim=None):
        """
        Show box and return pressed button.
        True if YES pressed, False if NO
        """

        if dim is None:
            dim = self.screen.get_cols_rows()
        while True:
            try:
                self.screen.draw_screen(dim, self.render(dim, True))

                _keys = self.screen.get_input()

                if [x for x in (self.keys.KEY_LEFT,
                                self.keys.KEY_RIGHT,
                                self.keys.KEY_UP,
                                self.keys.KEY_DOWN,
                                ) if x in _keys]:
                    self._change_focus(_keys)

                if self.keys.KEY_ESC in _keys:
                    return False

                if self.keys.KEY_ENTER in _keys:
                    _button = self._buttons.focus_cell.get_w()
                    self._pressed(_button)
                    return self._value
            except KeyboardInterrupt:
                continue

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _init_buttons(self):
        _yes_len = len(self._yes_txt)
        _no_len = len(self._no_txt)
        _b_attr = self._attr("button")
        _b_size = max(_yes_len, _no_len) + 4 # < ... >

        self._b_yes = lowui.AttrWrap(libxyz.ui.XYZButton(self._yes_txt),_b_attr)
        self._b_no = lowui.AttrWrap(libxyz.ui.XYZButton(self._no_txt),_b_attr)

        return lowui.GridFlow([self._b_yes, self._b_no], _b_size, 2, 0,
                              align.CENTER)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _change_focus(self, keys):
        """
        Move focus
        """

        for key in keys:
            _widget = None

            # Move right
            if key in (self.keys.KEY_RIGHT, self.keys.KEY_UP):
                _widget = 1 # index
            # Move left
            elif key in (self.keys.KEY_LEFT, self.keys.KEY_DOWN):
                _widget = 0
            else:
                pass

            if _widget is not None:
                self._buttons.set_focus(_widget)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _pressed(self, button):
        """
        Button pressed
        """

        _label = button.get_label()

        if _label == self._yes_txt:
            self._value = True
        else:
            self._value = False
