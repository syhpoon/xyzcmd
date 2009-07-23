#!/usr/bin/env python
#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2009
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

from distutils.core import setup

setup(
    name = "xyzcmd",
    version = "0.0.1 beta",
    scripts = ["xyzcmd"],
    packages = ["libxyz"],
    data_files = [
        ("share/xyzcmd/conf", ["conf/*"]),
        #TODO: ("share/doc/xyzcmd", ["doc/*"]),
        ("share/xyzcmd/plugins", ["plugins/*"]),
        ("share/xyzcmd/skins", ["skins/*"]),
        ],
    
    requires = ["urwid"],

    author = "Max E. Kuznecov",
    author_email = "syhpoon@syhpoon.name",
    description = "XYZCommander - Console file manager",
    url = "http://xyzcmd.syhpoon.name/",
    license = "LGPL",
    )
