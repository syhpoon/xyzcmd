#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008-2009
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

import libxyz.ui as uilib

from libxyz.ui import lowui
from libxyz.core.utils import bstring, ustring

class CopyBox(lowui.WidgetWrap):
    """
    Copy dialog
    """

    resolution = (u"box", u"widget")
    
    def __init__(self, xyz, srctxt, dst, caption):
        self.xyz = xyz
        self._attr = lambda name: self.xyz.skin.attr(self.resolution, name)
        self._keys = uilib.Keys()

        srclabel = lowui.Text(bstring(_(u"Source:")))
        srctxt = lowui.Text(bstring(srctxt))
        dstlabel = lowui.Text(bstring(_(u"Destination:")))

        self.dstw = lowui.AttrWrap(lowui.Edit(edit_text=ustring(dst),
                                              wrap='clip'),
                                   self._attr("input"))

        self.save_attrw = lowui.CheckBox(bstring(_(u"Save attributes")),
                                         state=True)
        self.follow_linksw = lowui.CheckBox(bstring(_(u"Follow links")))
        self.buttonsw = lowui.Columns([self.save_attrw, self.follow_linksw])

        spacer = lowui.Text(" ")
        msg = lowui.Text(
            bstring(_(u"TAB to cycle. ENTER to submit. ESCAPE to cancel")),
            align=uilib.align.CENTER)
        
        w = [
            srclabel,
            srctxt,
            spacer,
            dstlabel,
            self.dstw,
            spacer,
            self.buttonsw,
            uilib.Separator(),
            msg
            ]

        self.widgets = lowui.Pile(w)
        box = lowui.AttrWrap(lowui.Filler(self.widgets), self._attr("box"))

        self.widget = uilib.Border(box, caption, self._attr("title"),
                              self._attr("border"))
                              
        super(CopyBox, self).__init__(self.widget)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def show(self):
        def _setup(dim):
            width = int((dim[0] / 100.0) * 80)
            height = int((dim[1] / 100.0) * 40)
            
            mount = lowui.AttrWrap(lowui.Filler(lowui.Text(u"")),
                               self._attr(u"mount"))
            mount = lowui.Overlay(mount, self.xyz.top, uilib.align.CENTER,
                               width, uilib.align.MIDDLE, height)

            return lowui.Overlay(self.widget, mount, uilib.align.CENTER,
                                 width - 2, uilib.align.MIDDLE, height - 2)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def _focus_button(b):
            self.widgets.set_focus(self.buttonsw)
            self.buttonsw.set_focus(b)
            
            return b

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def _focus_edit():
            self.widgets.set_focus(self.dstw)
            
            return self.dstw

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        focus_data = {1: lambda: _focus_edit(),
                      2: lambda: _focus_button(self.save_attrw),
                      3: lambda: _focus_button(self.follow_linksw)
                      }
        focus = 1
        focusw = self.dstw
        
        dim = self.xyz.screen.get_cols_rows()
        box = _setup(dim)

        result = None

        while True:
            self.xyz.screen.draw_screen(dim, box.render(dim, True))

            _input = self.xyz.input.get()

            if self.xyz.input.WIN_RESIZE in _input:
                dim = self.xyz.screen.get_cols_rows()
                box = _setup(dim)
                continue

            if self._keys.TAB in _input:
                if focus >= len(focus_data):
                    focus = 1
                else:
                    focus +=1

                focusw = focus_data[focus]()
            elif self._keys.ESCAPE in _input:
                break
            elif self._keys.ENTER in _input:
                result = {
                    'dst': bstring(self.dstw.get_edit_text()),
                    'save_attributes': self.save_attrw.get_state(),
                    'follow_links': self.follow_linksw.get_state()
                    }
                break
            else:
                for k in _input:
                    focusw.keypress((dim[0],), k)

        return result
