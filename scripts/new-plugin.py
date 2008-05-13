#!/usr/bin/env python
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

"""
Create new plugin template
"""

import sys

def write_plugin(pname, author, ns):

    _template = """\
#-*- coding: utf8 -*
#
# Author <e-mail> year
#

from libxyz.core.plugins import BasePlugin

class XYZPlugin(BasePlugin):
    "%(pname)s"

    # Plugin name
    NAME = u"%(pname)s"

    # AUTHOR: Author name
    AUTHOR = u"%(author)s"

    # VERSION: Plugin version
    VERSION = u"0.1"

    # Brief one line description
    BRIEF_DESCRIPTION = u""

    # Full plugin description
    FULL_DESCRIPTION = u""

    # NAMESPACE: Plugin namespace. For detailed information about
    #            namespaces see Plugins chapter of XYZCommander user manual.
    #            Full namespace path to method is:
    #            xyz:plugins:misc:hello:SayHello

    NAMESPACE = "%(ns)s"

    def __init__(self, xyz):
        super(XYZPlugin, self).__init__(xyz)

        self.public = {}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def prepare(self):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def finalize(self):
        pass
""" % locals()
