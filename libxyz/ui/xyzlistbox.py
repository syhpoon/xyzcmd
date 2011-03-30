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
from libxyz.ui import Border
from libxyz.ui import Keys

class XYZListBox(lowui.WidgetWrap):
    """
    Simple list box
    """

    # Skin rulesets resolution order
    resolution = (u"list_box", u"box", u"widget")

    def __init__(self, xyz, body, walker, title, dim=None):
        """
        @param xyz: XYZ data
        @param body: Top-level widget
        @param walker: SimpleWalker or any walker-like instance
        @param title: ListBox title

        Required resources: title, border, box, selected
        """

        self.xyz = xyz

        if dim is None:
            _dim = self._get_dim()
        else:
            _dim = dim

        self._walker = walker
        self._keys = Keys()

        self.listbox = lowui.ListBox(walker)
        self.title = title
        self._listbox = lowui.AttrWrap(self.listbox, self._attr(u"box"))

        self._box = Border(self._listbox, title, self._attr(u"title"),
                           self._attr(u"border"))

        _box = lowui.Overlay(self._box, body, align.CENTER, _dim[0],
                             align.MIDDLE, _dim[1])

        super(XYZListBox, self).__init__(_box)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def show(self, dim=None, exit_keys=None, custom=None):
        """
        Show list

        @param custom: Function for custom key processing.
                       Accepted arguments: key and NumEntry instance of focused
                       entry.
                       If returns True - continue with internal processing
                       If returns False - next iteration
                       If returns None - exit
        """

        exit_keys = exit_keys or []

        if dim is None:
            dim = self.xyz.screen.get_cols_rows()

        while True:
            self.xyz.screen.draw_screen(dim, self.render(dim, True))

            _i = self.xyz.input.get()

            if self.xyz.input.WIN_RESIZE in _i:
                dim = self.xyz.screen.get_cols_rows()
                continue
                
            if _i:
                # Check if custom processing required
                if callable(custom):
                    (focus, _) = self.listbox.get_focus()

                    r = custom(_i, focus)

                    if r is None:
                        return
                    elif r == False:
                        continue

                for _k in _i:
                    if _k == self._keys.ESC:
                        return
                    elif _k == "j":
                        _k = self._keys.DOWN
                    elif _k == "k":
                        _k = self._keys.UP

                    self._listbox.keypress(dim, _k)

                    # Also quit on specified keys if any
                    if _k in exit_keys:
                        return

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def set_title(self, title):
        """
        Change title
        """

        self.title = title
        self._box.set_title(title)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def _attr(self, name):
        """
        Find palette
        """

        return self.xyz.skin.attr(self.resolution, name)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _get_dim(self):
        _dim = self.xyz.screen.get_cols_rows()

        return (_dim[0] - 4, _dim[1] - 4)
