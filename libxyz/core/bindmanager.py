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

import libxyz

class BindManager(object):
    """
    Key bindings management class
    """

    def __init__(self, xyz):
        self.xyz = xyz

        self._path_sel = libxyz.PathSelector()

        self._parse_config()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _parse_config(self):
        def _comment_cb(mo):
            return True

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def _from_cb(mo):
            _plugin = mo.group("plugin")
            _method = mo.group("method")

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def _load_cb(mo):
            return True

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def _bind_cb(mo):
            return True

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        _comment_re = re.compile("^\s*#.*$")

        _from_re = re.compile("""
        ^                  # begin
        \s*                # leading spaces
        from               # keyword from
        \s+                # one ore more spaces
        (?P<plugin>[\w:]+) # plugin ns-path
        \s+                # one ore more spaces
        load               # keywoard load
        \s+                # one ore more spaces
        (?P<method>\w+)    # method name
        \s*                # trailing spaces
        $                  # EOL
        """, re.VERBOSE)

        _load_re = re.compile("""
        ^                  # begin
        \s*                # leading spaces
        load               # keywoard load
        \s+                # one ore more spaces
        (?P<method>\w+)    # method name
        \s*                # trailing spaces
        $                  # EOL
        """, re.VERBOSE)

        _bind_re = re.compile("""
        ^                  # begin
        \s*                # leading spaces
        bind               # keywoard bind
        (?P<force>\!?)     # Optional ! (force) mark
        \s+                # one ore more spaces
        (?P<method>[\w:]+) # plugin ns-path and/or method name
        \s+                # one ore more spaces
        to                 # keyword to
        \s+                # one ore more spaces
        (?P<shortcut>\S+)  # shortcut
        \s*                # trailing spaces
        $                  # end
        """, re.VERBOSE)

        _cbpool = {_comment_re: _comment_cb,
                   _from_re: _from_cb,
                   _load_re: _load_cb,
                   _bind_re: _bind_cb,
                  }

        _parser = libxyz.parser.RegexpParser(_cbpool)
        _parser.parse(self._path_sel(const.KEYS_CONF_FILE))
