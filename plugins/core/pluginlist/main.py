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

import libxyz.ui as uilib

from libxyz.ui import lowui
from libxyz.core.plugins import BasePlugin

from entry import PluginEntry

class XYZPlugin(BasePlugin):
    """
    Show installed plugins
    """

    NAME = u"pluginlist"
    AUTHOR = u"Max E. Kuznecov ~syhpoon <mek@mek.uz.ua>"
    VERSION = u"0.1"
    BRIEF_DESCRIPTION = u"Show plugin list"
    FULL_DESCRIPTION = u"Show all currently loaded plugins and assosiated "\
                       u"information"
    NAMESPACE = u"core"

    def __init__(self, xyz):
        super(XYZPlugin, self).__init__(xyz)

        self.public = {"show_list": self._show_list}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _show_list(self):
        """
        Show plugins list
        """

        _plugins = sorted(self.xyz.pm.get_all_loaded().values(),
                          lambda x, y: cmp(x.ns, y.ns))

        self._walker = lowui.SimpleListWalker([
                           PluginEntry(_obj, self.xyz.skin.attr, self._info)
                           for _obj in _plugins])

        _list = uilib.XYZListBox(self.xyz, self.xyz.top, self._walker,
                                 _(u"Active plugins list"))
        _list.show()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _info(self):
        """
        Show plugin detailed info
        """

        _w = self._walker.get_focus()[0]
        _plugin = _w.plugin

        uilib.MessageBox(self.xyz, self.xyz.top, "%s" %
          str([(k, v.__doc__) for k,v in _plugin.public.iteritems()])).show()
