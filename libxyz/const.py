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
Constants
"""

import sys
import os

# Project name
PROG = u"XYZCommander"

# Project homepage
HOMEPAGE = u"xyzcmd.syhpoon.name"

# User directory
USER_DIR = u".xyzcmd"

# System directory prefix
SYSTEM_PREFIX = os.getenv("XYZCMD_PREFIX", sys.prefix)

# System directory
SYSTEM_DIR = os.path.join(SYSTEM_PREFIX, "share/xyzcmd")

# Subdirectory with configuration files
CONF_DIR = u"conf"

# Plugins subdirectory
PLUGINS_DIR = u"plugins"

# Skins subdirectory
SKINS_DIR = u"skins"

# Locale subdirectory
LOCALE_DIR = u"locale"

# Main configuration file name
XYZ_CONF_FILE = u"main.xyz"

# Keybindings configuration file name
KEYS_CONF_FILE = u"keys.xyz"

# Plugins configuration file name
PLUGINS_CONF_FILE = u"plugins.xyz"

# Actions configuration file name
ACTIONS_CONF_FILE = u"actions.xyz"

# Aliases configuration file name
ALIASES_CONF_FILE = u"aliases.xyz"

# Internal commands configuration file name
ICMD_CONF_FILE = u"icmd.xyz"

# VFS configuration file name
VFS_CONF_FILE = u"vfs.xyz"

# Hooks configuration file name
HOOKS_CONF_FILE = u"hooks.xyz"

# Default fallback skin name
DEFAULT_SKIN = u"seablue"

# Default display driver. raw or curses
DEFAULT_DISPLAY_DRIVER = u"raw"
