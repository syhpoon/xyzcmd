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
from libxyz.core import Queue
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
    EVENTS = [("show",
               "Fires upon showing console. Arguments: No."),
              ("cmd_prev",
               "Fires when scrolling through history. "\
               "Arguments: Current command from history buffer"),
              ("execute",
               "Fires when typed command is to be executed. "\
               "Arguments: typed command"),
        ]

    def __init__(self, xyz):
        super(XYZPlugin, self).__init__(xyz)

        self.attr = lambda x: self.xyz.skin.get_palette(u"plugin.console", x)

        self._keys= ui.Keys()
        self._index = 1
        self.output = []
        self.edit = lowui.Edit(self.conf["prompt"], wrap="clip")
        self._input = lowui.AttrWrap(self.edit, self.attr("input"))
        self._header = lowui.AttrWrap(lowui.Text(_(u"Management console")),
                                      self.attr("header"))
        self._history = Queue(self.conf["history_depth"])

        self.export(self.show)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def show(self):
        """
        Show console window
        """

        def _get_cmd(k):
            """
            Fetch previous command from history
            """
            
            _i = -1 if k == self._keys.UP else 1
            
            _pos = len(self._history) - 1 + (self._index + _i)
            
            if _pos < 0:
                return None
            elif _pos > len(self._history):
                return None
            else:
                self._index += _i
                
            if _pos == len(self._history):
                return ""

            try:
                cmd = self._history[_pos]
            except Exception:
                return None
            else:
                return cmd

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.fire_event("show")
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
                if k in (self._keys.UP, self._keys.DOWN):
                    cmd = _get_cmd(k)

                    if cmd is not None:
                        self.fire_event("cmd_prev", cmd)
                        self.edit.set_edit_text("")
                        self.edit.insert_text(cmd)
                elif k == self._keys.ENTER:
                    self._index = 1
                    chunk = self.edit.get_edit_text()
                    self.edit.set_edit_text("")
                    compiled = None

                    if not chunk:
                        continue

                    self._history.push(chunk)
                    
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
                            self.fire_event("execute", chunk)
                            
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
