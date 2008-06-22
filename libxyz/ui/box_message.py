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

class MessageBox(Box):
    """
    Simple box is used to display any kind of text messages
    Show the message until any key pressed
    """

    resolution = (u"message_box", u"box", u"widget")

    def __init__(self, xyz, body, message, title="", width=60):
        """
        @param xyz: XYZ data
        @param body: Top-level widget
        @param message: Message to display
        @param title: Box title
        @param width: Box width (including mount box)

        Required resources: title, box, border, mount
        """

        super(MessageBox, self).__init__(xyz, body, message, title, width)
        self.calc_size(5)

        _title = self._strip_title(title.replace(u"\n", u" "))

        if _title:
            _title = (_title, self._attr(u"title"))
        else:
            _title = None

        _mount = lowui.AttrWrap(lowui.Filler(lowui.Text(u"")),
                                self._attr(u"mount"))

        _text = lowui.Text(message, align.CENTER)
        _box = lowui.Filler(_text)
        _box = Border(_box, _title, self._attr(u"border"))
        _box = lowui.AttrWrap(_box, self._attr(u"box"))

        _mount = lowui.Overlay(_mount, body, align.CENTER, self.full_width,
                             align.MIDDLE, self.full_height)

        _box = lowui.Overlay(_box, _mount, align.CENTER, self.box_width,
                             align.MIDDLE, self.box_height)

        self.parent_init(_box)
