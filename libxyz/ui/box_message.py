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

class MessageBox(lowui.WidgetWrap):
    """
    Simple box is used to display any kind of text messages
    Show the message until any key pressed
    """

    # Skin rulesets resolution order
    resolution = (u"message_box", u"box", u"widget")

    def __init__(self, xyz, body, message, title="", width=60):
        """
        @param xyz: XYZ data
        @param body: Top-level widget
        @param message: Message to display
        @param title: Box title
        @param width: Box width (including mount box)

        Required resources: title, box, mount
        """

        self.screen = xyz.screen
        self.skin = xyz.skin
        self.rowspan = 3
        self.mount_span = {u"vertical": 2, u"horizontal": 2}
        self.full_width = width
        self.box_width = width - self.mount_span[u"horizontal"]
        self.box_height = self._rows(message)
        self.full_height = self.box_height + self.mount_span[u"vertical"]

        _title = lowui.Text((self._attr(u"title"),
                             " %s "  % title.replace(u"\n", u"")), align.CENTER)

        _mount = lowui.AttrWrap(lowui.Filler(_title, align.TOP),
                                self._attr(u"mount"))

        _text = lowui.Text(message, align.CENTER)
        _box = lowui.AttrWrap(lowui.Filler(_text), self._attr(u"box"))

        _mount = lowui.Overlay(_mount, body, align.CENTER, self.full_width,
                             align.MIDDLE, self.full_height)

        _box = lowui.Overlay(_box, _mount, align.CENTER, self.box_width,
                             align.MIDDLE, self.box_height)

        super(MessageBox, self).__init__(_box)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def show(self, dim):
        """
        Show box
        """

        self.screen.draw_screen(dim, self.render(dim, True))

        while not self.screen.get_input():
            pass

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
                   2 - self.mount_span[u"vertical"]
        _lines = msg.count("\n")

        if _lines + self.rowspan > _maxrows:
            _rows = _maxrows
        else:
            _rows = _lines + self.rowspan

        return _rows
