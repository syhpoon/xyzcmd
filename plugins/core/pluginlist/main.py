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

import inspect

import libxyz.ui as uilib

from libxyz.ui import lowui
from libxyz.core.plugins import BasePlugin

from entry import PluginEntry

class XYZPlugin(BasePlugin):
    """
    Show installed plugins
    """

    NAME = u"pluginlist"
    AUTHOR = u"Max E. Kuznecov ~syhpoon <syhpoon@syhpoon.name>"
    VERSION = u"0.1"
    BRIEF_DESCRIPTION = u"Show plugin list"
    FULL_DESCRIPTION = u"Show all currently loaded plugins and associated "\
                       u"information"
    NAMESPACE = u"core"
    HOMEPAGE = u"xyzcmd.syhpoon.name"

    def __init__(self, xyz):
        super(XYZPlugin, self).__init__(xyz)

        self.export(u"show_list", self.show_list)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def show_list(self):
        """
        Show plugins list
        """

        _plugins = sorted(self.xyz.pm.get_all_loaded().values(),
                          lambda x, y: cmp(x.ns, y.ns))

        _sel_attr = self.xyz.skin.attr(uilib.XYZListBox.resolution, u"selected")
        self._walker = lowui.SimpleListWalker([PluginEntry(_obj, _sel_attr,
                                              self._info) for _obj in _plugins])

        uilib.XYZListBox(self.xyz, self.xyz.top, self._walker,
                         _(u"Active plugins list")).show()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _info(self):
        """
        Show plugin detailed info
        """

        def _add_info():
            if _plugin.AUTHOR is not None:
                _data.append(lowui.Text(_(u"Author: %s" % _plugin.AUTHOR)))

            if _plugin.VERSION is not None:
                _data.append(lowui.Text(_(u"Version: %s" % _plugin.VERSION)))

            if _plugin.MIN_XYZ_VERSION is not None:
                _data.append(lowui.Text(_(u"Minimal compatible version: %s"
                                          % _plugin.MIN_XYZ_VERSION)))

            if _plugin.HOMEPAGE is not None:
                _data.append(lowui.Text(_(u"Homepage: %s" % _plugin.HOMEPAGE)))

            _data.append(_div)

            if _plugin.FULL_DESCRIPTION is not None:
                _data.append(lowui.Text(_plugin.FULL_DESCRIPTION))

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def make_args(func):
            _args, _varargs, _varkw, _def = inspect.getargspec(func)

            # We will be inspecting only methods, so always skip self
            if len(_args) == 1:
                return u""

            _args = _args[1:]
            _tmp = []

            # No defaults
            if _def is None:
                _tmp = _args
            else:
                _delta = len(_args) - len(_def)

                if _delta > 0:
                    _tmp.extend(_args[:_delta])
                    _args = _args[_delta:]

                for _a, _d in zip(_args, _def):
                    _tmp.append(u"=".join((unicode(_a), unicode(_d))))

            return u",".join(_tmp)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def _add_public_data():
            if _plugin.public_data:
                _data.append(uilib.Separator(_(u"Public data"),
                                             title_attr=_titleattr,
                                             div_attr=_divattr))

                _dlen = len(_plugin.public_data)
                _di = 0

                for k, v in _plugin.public_data.iteritems():
                    _data.append(lowui.Text(u"%s: %s" % (k, type(v))))

                    _di += 1

                    if _di < _dlen:
                        _data.append(_div)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def _add_public_methods():
            _data.append(uilib.Separator(_(u"Public methods"),
                                         title_attr=_titleattr,
                                         div_attr=_divattr))

            _len = len(_plugin.public)
            _i = 0

            for k in sorted(_plugin.public.keys()):
                v = _plugin.public[k]

                if v.__doc__ is not None:
                    _doc = v.__doc__.rstrip()
                else:
                    _doc = v.__doc__

                _data.append(lowui.Text(u"%s(%s): %s" %
                             (k, make_args(v), _doc)))

                _i += 1

                if _i < _len:
                    _data.append(_div)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        _w = self._walker.get_focus()[0]
        _plugin = _w.plugin

        _divattr = self.xyz.skin.attr(uilib.XYZListBox.resolution, u"border")
        _titleattr = self.xyz.skin.attr(uilib.XYZListBox.resolution, u"title")
        _div = lowui.Text("")

        _data = []

        _add_info()

        if _plugin.DOC is not None:
            _data.append(uilib.Separator(_(u"Plugin doc"),
                                         title_attr=_titleattr,
                                         div_attr=_divattr))

            _data.append(lowui.Text(_plugin.DOC))

        _add_public_data()
        _add_public_methods()

        _method_walker = lowui.SimpleListWalker(_data)

        uilib.XYZListBox(self.xyz, self.xyz.top, _method_walker,
                         _(u"Plugin info %s" % _plugin.ns)).show()
