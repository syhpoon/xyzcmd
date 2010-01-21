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

from libxyz.ui import lowui
from libxyz.ui import align
from libxyz.ui import Box
from libxyz.ui import Border

import libxyz.ui

class ButtonBox(Box):
    """
    Button box. Shows a message and waits for button pressed
    """

    # Skin rulesets resolution order
    resolution = (u"button_box", u"box", u"widget")

    def __init__(self, xyz, body, message, buttons, title="", width=70):
        """
        @param xyz: XYZ dictionary
        @param body: Top-level widget
        @param message: Message to display
        @param buttons: List of button pairs (text, value).
                        Text is what button shows and value is what
                        being returned.
        @param title: Box title
        @param width: Box width (including mount box)

        Required resources: title, box, border, mount, button
        """

        super(ButtonBox, self).__init__(xyz, body, message, title, width)
        self.calc_size(6)

        self.buttons = buttons
        self.keys = libxyz.ui.Keys()
        self._buttons = self._init_buttons(self.buttons)

        _title = self._strip_title(title.replace(u"\n", u" "))

        if _title:
            _title_attr = self._attr(u"title")
        else:
            _title = None
            _title_attr = None

        _mount = lowui.AttrWrap(lowui.Filler(lowui.Text(u"")),
                                self._attr(u"mount"))

        # Main dialog text
        _text = lowui.Text((self._attr(u"box"), message), align.CENTER)
        _blank = lowui.Text((self._attr(u"box"), ""))

        _widgets = [_text, _blank, self._buttons]
        _box = lowui.Filler(lowui.Pile(_widgets), valign=align.BOTTOM)
        _box = Border(_box, _title, _title_attr, self._attr(u"border"))
        _box = lowui.AttrWrap(_box, self._attr(u"box"))

        _mount = lowui.Overlay(_mount, body, align.CENTER, self.full_width,
                             align.MIDDLE, self.full_height)
        _box = lowui.Overlay(_box, _mount, align.CENTER, self.box_width,
                             align.MIDDLE, self.box_height)

        self.parent_init(_box)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def show(self, dim=None):
        """
        Show box and return pressed button value.
        """

        if dim is None:
            dim = self.screen.get_cols_rows()
        while True:
            try:
                self.screen.draw_screen(dim, self.render(dim, True))

                _keys = self.xyz.input.get()

                if self.xyz.input.WIN_RESIZE in _keys:
                    dim = self.screen.get_cols_rows()
                    continue

                if [x for x in (self.keys.LEFT,
                                self.keys.RIGHT,
                                self.keys.UP,
                                self.keys.DOWN,
                                ) if x in _keys]:
                    self._change_focus(_keys)

                if self.keys.ESCAPE in _keys:
                    return None

                if self.keys.ENTER in _keys:
                    _button = self._buttons.focus_cell.get_w()
                    return self._pressed(_button)
            except KeyboardInterrupt:
                continue

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _init_buttons(self, buttons):
        _b_attr = self._attr("button")
        _actb_attr = self._attr("button_active")
        
        _b_size = max([len(b[0]) for b in buttons]) + 4 # [ ... ]

        data = [lowui.AttrWrap(libxyz.ui.XYZButton(x[0]), _b_attr)
                for x in buttons]

        buttons = lowui.GridFlow(data, _b_size, 2, 0, align.CENTER)
        buttons.focus_cell.set_attr(_actb_attr)

        return buttons

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _change_focus(self, keys):
        """
        Move focus
        """

        _inact = self._attr("button")
        _act = self._attr("button_active")

        _cells = self._buttons.cells
        _index = lambda: _cells.index(self._buttons.focus_cell)
        
        for key in keys:
            _widget = None

            # Move right
            if key in (self.keys.RIGHT, self.keys.UP):
                i = _index()
                
                if i < len(_cells) - 1:
                    _widget = i + 1 # index
                else:
                    _widget = 0
            # Move left
            elif key in (self.keys.LEFT, self.keys.DOWN):
                i = _index()
                
                if i > 0:
                    _widget = i - 1
                else:
                    _widget = len(_cells) - 1
            else:
                pass

            if _widget is not None:
                self._buttons.focus_cell.set_attr(_inact)
                self._buttons.set_focus(_widget)
                self._buttons.focus_cell.set_attr(_act)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _pressed(self, button):
        """
        Button pressed
        """

        _label = button.get_label()

        for txt, val in self.buttons:
            if _label == txt:
                return val

        return None
