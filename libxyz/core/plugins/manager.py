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

import sys
import re
import os
import os.path

from libxyz.exceptions import PluginError, XYZValueError
from libxyz.parser import FlatParser

class PluginManager(object):
    """
    Plugin manager class
    It is supposed to:
    - Scan for plugin dirs
    - Load and parse found plugins
    - Provide easy access to plugins data
    """

    NAMESPACES = (u"misc", u"ui", u"vfs")

    def __init__(self, dirs):
        """
        @param dirs: Plugin directories list
        @type dirs: list
        """

        if type(dirs) != type([]):
            raise XYZValueError(_(u"Invalid argument type %s. List expected" %
                                  type(dirs)))
        else:
            self.dirs = dirs
            sys.path.extend(dirs)

        self.required_metavars = (u"AUTHOR",
                                  u"VERSION",
                                  u"BRIEF_DESCRIPTION",
                                  u"FULL_DESCRIPTION",
                                  )

        self.optional_metavars = (u"MIN_XYZ_VERSION",)

        self.metavars = []
        self.metavars.extend(self.required_metavars)
        self.metavars.extend(self.optional_metavars)

        # Try to load all activated plugins
        self._load(self._activated_plugins)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _load(self, active_list):
        """
        Try to load plugins
        """

        for _plugin in active_list:
            if os.path.isdir(_plugin):
                self._load_plugin_dir(_plugin)
            else: # WTF?
                raise PluginError(_(u"Unable to load plugin: %s" % _plugin))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _load_plugin_dir(self, plugin):
        # Import plugin's main
        try:
            _loaded = __import__(plugin, globals(), locals(), ["main"])
        except ImportError, e:
            raise PluginError(_(u"Unable to load plugin %s: %s" % (plugin, e))

        for _required in self.required_metavars:
            if _required not in _parsed:
                raise PluginError(_(u"Required variable not defined in "\
                                    u"meta-file: %s" % _required))

        # 4. Import plugin module
        module = __import__()
