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

class InputBox(Box):
    """
    Shows a message and waits for input
    """

    # Skin rulesets resolution order
    resolution = (u"input_box", u"box", u"widget")

    def __init__(self, xyz, body, message, title="", text="", width=70):
        """
        @param xyz: XYZ dictionary
        @param body: Top-level widget
        @param message: Message to display
        @param title: Box title
        @param width: Box width (including mount box)

        Required resources: title, box, border, mount, input, button
        """

        super(InputBox, self).__init__(xyz, body, message, title, width)
        self.calc_size(7)

        self.keys = libxyz.ui.Keys()

        _hint = lowui.Text(_(u"Press ENTER to submit value. ESCAPE to quit"),
                           align=align.CENTER)

        _title = self._strip_title(title.replace(u"\n", u" "))

        if _title:
            _title = (_title, self._attr(u"title"))
        else:
            _title = None

        _mount = lowui.AttrWrap(lowui.Filler(lowui.Text(u"")),
                                self._attr(u"mount"))

        # Main dialog text
        _text = lowui.Text((self._attr(u"box"), message), align.CENTER)
        _blank = lowui.Text((self._attr(u"box"), ""))

        self._edit = lowui.AttrWrap(lowui.Edit(wrap="clip", edit_text=text),
                                    self._attr(u"input"))

        _widgets = [_text, _blank, self._edit, _blank, _hint]
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
        Show box and return input value.
        Return None if Escape was pressed
        """

        if dim is None:
            dim = self.screen.get_cols_rows()
        while True:
            try:
                self.screen.draw_screen(dim, self.render(dim, focus=True))

                _keys = self.xyz.input.get()

                if self.keys.ESCAPE in _keys:
                    return None

                if self.keys.ENTER in _keys:
                    return self._edit.get_edit_text()

                for k in _keys:
                    self._edit.keypress((dim[0],), k)
            except KeyboardInterrupt:
                continue
