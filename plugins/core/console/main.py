#-*- coding: utf8 -*
#
# Max E. Kuznecov <syhpoon@syhpoon.name> 2008-2009
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

from libxyz.core.plugins import BasePlugin
from libxyz.core import dsl
from libxyz.core.utils import bstring
from libxyz.ui import lowui

import libxyz.ui as ui

class XYZPlugin(BasePlugin):
    "Plugin console"

    NAME = u"console"
    AUTHOR = u"Max E. Kuznecov <syhpoon@syhpoon.name>"
    VERSION = u"0.1"
    BRIEF_DESCRIPTION = u"Interactive management console"
    FULL_DESCRIPTION = u"Provides interactive management console"
    NAMESPACE = u"core"

    def __init__(self, xyz):
        super(XYZPlugin, self).__init__(xyz)

        self.attr = lambda x: self.xyz.skin.get_palette(u"plugin.console", x)

        self._keys= ui.Keys()
        self.output = []
        self.edit = lowui.Edit("> ", wrap="clip")
        self._input = lowui.AttrWrap(self.edit, self.attr("input"))
        self._header = lowui.AttrWrap(lowui.Text(_(u"Management console")),
                                      self.attr("header"))

        self.export(self.show)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def show(self):
        """
        Show console window
        """

        _stop = False

        while True:
            walker = lowui.SimpleListWalker(self.output)
            walker.focus = len(walker) - 1
            lbox = lowui.AttrWrap(lowui.ListBox(walker), self.attr("output"))
        
            console = lowui.Frame(lbox, header=self._header,
                                  footer=self._input, focus_part='footer')
            dim = self.xyz.screen.get_cols_rows()

            self.xyz.screen.draw_screen(dim, console.render(dim, True))

            data = self.xyz.input.get()

            for k in data:
                if k == self._keys.ENTER:
                    chunk = self.edit.get_edit_text()
                    self.edit.set_edit_text("")
                    compiled = None

                    self._write("> %s" % chunk)
                    
                    try:
                        compiled = compile(chunk, "<input>", "eval")
                    except Exception, e:
                        self._write(str(e))
                        break
                    else:
                        # Incomplete
                        if compiled is None:
                            break
                        else:
                            chunk = ""
                            try:
                                self._write(
                                    eval(compiled, dsl.XYZ.get_env()))
                            except Exception, e:
                                self._write(str(e))

                elif k == self._keys.ESCAPE:
                    _stop = True
                    break
                else:
                    self._input.keypress((dim[0],), k)

            if _stop:
                break

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _write(self, msg):
        """
        Write text to output
        """

        self.output.extend([lowui.Text(x) for x in bstring(msg).split("\n")])
