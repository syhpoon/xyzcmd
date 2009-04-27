#!/usr/bin/env/python
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

setup(name = "xyzcmd",
      version = "0.0.1alpha2",
      description = "XYZCommander - Console file manager",
      author = "Max E. Kuznecov",
      author_email = "syhpoon@syhpoon.name",
      url = "http://xyzcmd.syhpoon.name",
      packages = ["libxyz"],
      scripts = ["pyrrdp-run.py", "pyrrdp-httpd-run.py"],
      data_files = [('etc', ['pyrrdp.conf']),
                    ('/var/db/pyrrdp', []),
                    ('www/pyrrdp', []),
                    ('share/pyrrdp/templates',
                     ['templates/about.template',
                      'templates/head.template',
                      'templates/detail.template',
                      'templates/index.template',
                      'templates/group.template',
                      'templates/logo.png.template',
                      'templates/pyrrdp.css.template',
                      ]),
                    ]
      )

