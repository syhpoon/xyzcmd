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

import re
import os
import os.path

from libxyz.exceptions import PluginError
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
    PLUGIN_EXT = (re.compile(u"\.zip$", re.U),
                       re.compile(u"\.tar$", re.U),
                       re.compile(u"\.tar\.gz$", re.U),
                       re.compile(u"\.tar\.bz2$", re.U),
                      )

    def __init__(self, dirs):
        """
        @param dirs: Plugin directories list
        @type dirs: sequence
        """

        self.metafile = u"meta"
        self._raw_plugin_list = []

        _meta_opt = {u"validvars": (u"AUTHOR",
                                    u"VERSION",
                                    u"BRIEF_DESCRIPTION",
                                    u"FULL_DESCRIPTION",
                                    u"MIN_XYZ_VERSION",
                                    ),
                    }

        self._meta_parser = FlatParser(_meta_opt)

        # First scan for available plugins
        for _dir in dirs:
            self._raw_plugin_list.extend(self._scan(_dir))

        # Next try to load all activated plugins
        self._load(self._raw_plugin_list)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _scan(self, pdir):
        """
        Scan directory for plugins
        Return list of plugin derectories and archives inside
        It doesn't check for plugin validity, only for matching criteria
        of directory/archive to be recognized as plugin.
        """

        _result = []

        # The directory to be recognized as plugin must contain:
        # 1) file named `meta'
        # 2) file named as directory it's being held inside with .py extension

        # Also all supported archives are recognized as plugins

        # Searching is performed in subdirectories of supplied directory
        # named according to available namespaces.

        for _nsdir in [os.path.join(pdir, _ns) for _ns in self.NAMESPACES]:
            _walk = os.walk(_nsdir)
            try:
                _root, _dirs, _files = _walk.next()
            except StopIteration:
                continue

            for _dir in _dirs:
                _basedir = os.path.join(_nsdir, _dir)

                _pluginfile = os.path.join(_basedir, u"%s.py" % _dir)
                _metafile = os.path.join(_basedir, self.metafile)

                if os.access(_metafile, os.R_OK) and \
                os.access(_pluginfile, os.R_OK):
                    _result.append(_basedir)

            # Add matchin archives
            _result.extend([
                            os.path.join(_nsdir, _file) for _file in _files
                            if len(filter(None,
                                [
                                  regexp.search(_file)
                                  for regexp in self.PLUGIN_EXT
                                ]))
                            ])

        return _result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _load(self, raw_list):
        """
        Try to load plugins
        """

        for _plugin in raw_list:
            if os.path.isdir(_plugin):
                self._load_plugin_dir(_plugin)
            elif os.path.isfile(_plugin):
                self._load_plugin_file(_plugin)
            else: # WTF?
                raise PluginError(_(u"Unable to load plugin: %s" % _plugin))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _load_plugin_dir(self, plugin):
        try:
            _meta_file = open(os.path.join(plugin, self.metafile), "r")
        except IOError, e:
            raise PluginError(_(u"Unable to open meta-file: %s" % e))

        try:
            self._meta_parser.parse(_meta_file)
        except ParseError,e :
            raise PluginError(_(u"Error parsing meta-file: %s" % e))
