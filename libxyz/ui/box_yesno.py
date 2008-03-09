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
        """

        self.screen = xyz.screen
        self.skin = xyz.skin
        self.rowspan = 3
        self.mount_span = {"vertical": 2, "horizontal": 2}
        self.full_width = width
        self.box_width = width - self.mount_span["horizontal"]
        self.box_height = self._rows(message) + 1 # buttons
        self.full_height = self.box_height + self.mount_span["vertical"]
        
        _b_yes = lowui.Button(_("Yes"))
        _b_no = lowui.Button(_("No"))
        _bgrid = lowui.GridFlow([_b_yes, _b_no], 10, 2, 0, align.CENTER)

        _title = lowui.Text((self._attr('title'),
                             " %s "  % title.replace("\n", "")), align.CENTER)

        _mount = lowui.AttrWrap(lowui.Filler(_title, align.TOP),
                                self._attr('mount'))

        _buttons = lowui.AttrWrap(lowui.Filler(_bgrid, align.BOTTOM),
                                  self._attr('box'))

        _text = lowui.Text(message, align.CENTER)
        _text = lowui.AttrWrap(lowui.Filler(_text), self._attr('box'))
        _box = lowui.Pile([_text, _buttons])

        _mount = lowui.Overlay(_mount, body, align.CENTER, self.full_width,
                             align.MIDDLE, self.full_height)

        _box = lowui.Overlay(_box, _mount, align.CENTER, self.box_width,
                             align.MIDDLE, self.box_height)

        super(YesNoBox, self).__init__(_box)

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

        # 2 for two rows: on top and bottom
        _maxrows = self.screen.get_cols_rows()[1] - \
                   2 - self.mount_span["vertical"]
        _lines = msg.count("\n")

        if _lines + self.rowspan > _maxrows:
            _rows = _maxrows
        else:
            _rows = _lines + self.rowspan

        return _rows
