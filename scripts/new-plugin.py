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

import os
import os.path
import sys

template = """\
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
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def error(em):
    print "ERROR: %s" % em
    sys.exit(1)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def write_plugin(pname, author, ns):
    global template

    _cont = template % locals()

    # Create plugin directory
    try:
        os.mkdir("./%s" % pname)
    except OSError, e:
        error("Unable to create plugin directory %s: %s" % (pname, str(e)))

    # Create neccesary files

    file("./%s/__init__.py" % pname, "w").close()

    main = file("./%s/main.py" % pname, "w")
    main.write("%s\n" % _cont)
    main.close()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def usage():
    print "%s plugin_name author namespace" % os.path.basename(sys.argv[0])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":
    if len(sys.argv) != 4:
        usage()
        sys.exit(1)
    else:
        pname, author, ns = sys.argv[1:]

    write_plugin(pname, author, ns)

    print "Plugin template created"
