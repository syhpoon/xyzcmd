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

class YesNoBox(lowui.WidgetWrap):
    """
    Yes/No box. Shows a message and waits for Yes or No button pressed
    """

    # Skin rulesets resolution order
    resolution = ("yesno_box", "box", "widget")

    def __init__(self, xyz, body, message, title="", width=60):
        """
        @param xyz: XYZ dictionary
        @param body: Top-level widget
        @param message: Message to display
        @param title: Box title
        @param width: Box width (including mount box)

        Required resources: title, box, mount, button
        """

        self.screen = xyz.screen
        self.skin = xyz.skin
        self.rowspan = 3
        self.mount_span = {"vertical": 2, "horizontal": 2}
        self.full_width = width
        self.box_width = width - self.mount_span["horizontal"]
        self.box_height = self._rows(message)
        self.full_height = self.box_height + self.mount_span["vertical"]

        _buttons = self._init_buttons()

        _title = lowui.Text((self._attr(u"title"),
                             " %s "  % title.replace("\n", "")), align.CENTER)
        _mount = lowui.AttrWrap(lowui.Filler(_title, align.TOP),
                                self._attr(u"mount"))

        # Main dialog text
        _text = lowui.Text((self._attr(u"box"), message), align.CENTER)
        _blank = lowui.Text((self._attr(u"box"), ""))

        _mount = lowui.Overlay(_mount, body, align.CENTER, self.full_width,
                             align.MIDDLE, self.full_height)

        _widgets = [_text, _blank, _buttons]
        _box = lowui.AttrWrap(lowui.Filler(lowui.Pile(_widgets)),
                              self._attr(u"box"))
        _box = lowui.Overlay(_box, _mount, align.CENTER, self.box_width,
                             align.MIDDLE, self.box_height)

        super(YesNoBox, self).__init__(_box)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def show(self, dim):
        """
        Show box and return pressed button.
        True if YES pressed, False if NO
        """

        while True:
            self.screen.draw_screen(dim, self.render(dim, True))

            keys = self.screen.get_input()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _attr(self, name):
        """
        Find palette
        """

        return self.skin.attr(self.resolution, name)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _rows(self, msg):
        """
        Calculate required rows
        """

        # 2 for two rows: on top and bottom +
        _maxrows = self.screen.get_cols_rows()[1] - \
                   2 - self.mount_span["vertical"]
        _lines = msg.count("\n")

        if _lines + self.rowspan > _maxrows:
            _rows = _maxrows
        else:
            _rows = _lines + self.rowspan

        return _rows

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _init_buttons(self):
        _yes_txt = _(u"Yes")
        _no_txt = _(u"No")
        _yes_len = len(_yes_txt)
        _no_len = len(_no_txt)
        _b_attr = self._attr("button")
        _b_size = max(_yes_len, _no_len) + 4 # < ... >

        _b_yes = lowui.AttrWrap(lowui.Button(_yes_txt), _b_attr)
        _b_no = lowui.AttrWrap(lowui.Button(_no_txt), _b_attr)

        return lowui.GridFlow([_b_yes, _b_no], _b_size, 2, 0, align.CENTER)
