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

"""
Class is used to select first appropriate path.
"""

import os
import os.path

from libxyz import const

class PathSelector(object):
    """
    Class is used to select first appropriate path.
    Common rule is to load system file first and then user's one
    """

    def __init__(self):
        self.user_dir = os.path.join(os.path.expanduser("~"), const.USER_DIR)
        self.system_dir = const.SYSTEM_DIR
        self.conf_dir = const.CONF_DIR
        self.skins_dir = const.SKINS_DIR
        self.plugins_dir = const.PLUGINS_DIR
        self.locale_dir = const.LOCALE_DIR

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_conf(self, conf):
        """
        Return tuple of (system_conf_path, user_conf_path)
        """

        return self._get(self.conf_dir, conf)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_skin(self, skin):
        """
        Return tuple of (system_skin_path, user_skin_path)
        """

        return self._get(self.skins_dir, skin)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _get(self, subdir, obj):
        _userpath = os.path.join(self.user_dir, subdir, obj)
        _systempath = os.path.join(self.system_dir, subdir, obj)

        return (_systempath, _userpath)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_first_of(self, files):
        """
        Return first existing file from supplied files or False in none exist
        """

        for _file in files:
            if os.access(_file, os.R_OK):
                return _file

        return None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_plugins_dir(self):
        _userpath = os.path.join(self.user_dir, self.plugins_dir)
        _systempath = os.path.join(self.system_dir, self.plugins_dir)

        return [_userpath, _systempath]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_skins_dir(self):
        _userpath = os.path.join(self.user_dir, self.skins_dir)
        _systempath = os.path.join(self.system_dir, self.skins_dir)

        return [_userpath, _systempath]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_locale_dir(self):
        return os.path.join(self.system_dir, self.locale_dir)
