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

    def __init__(self, screen, body, message, title=None):
        """
        @param screen: Display instance
        @param body: ???
        @param message: Message
        @param title: Box title
        """

        _msg = lowui.AttrWrap(lowui.Filler(lowui.Padding(lowui.Text(message), align.CENTER, 20)), 'bg')
        _overlay = lowui.Overlay(_msg, body, align.CENTER, 15, align.MIDDLE, 5)

        super(MessageBox, self).__init__(_overlay)
