#-*- coding: utf8 -*
#
# Max E. Kuznecov <syhpoon@syhpoon.name> 2009
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
import subprocess

from libxyz.core import FSRule
from libxyz.core.plugins import BasePlugin

class XYZPlugin(BasePlugin):
    "Magic database FSRule"

    NAME = u"magic"
    AUTHOR = u"Max E. Kuznecov <syhpoon@syhpoon.name>"
    VERSION = u"0.1"
    BRIEF_DESCRIPTION = u"Magic database FSRule"
    FULL_DESCRIPTION = _(u"Plugin extends FSRule functionality to match "\
                         u"objects based on magic database description")
    NAMESPACE = u"fsrules"
    MIN_XYZ_VERSION = None
    DOC = None
    HOMEPAGE = "http://xyzcmd.syhpoon.name"

    def __init__(self, xyz):
        super(XYZPlugin, self).__init__(xyz)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def prepare(self):
        FSRule.extend("magic", self._transform, self._match)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def finalize(self):
        FSRule.unextend("magic")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _transform(self, arg):
        """
        Transformation function for magic FSRule
        """

        # Treat input argument as a regular expression to match on
        #`file` output
        
        return re.compile(arg, re.I)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _match(self, vfsobj, arg):
        """
        Match function for magic
        """
        
        try:
            result = subprocess.Popen([
                "/usr/bin/env", "file", "-b",
                vfsobj.path], stdout=subprocess.PIPE).communicate()[0].strip()

            return arg.search(result) is not None
        except Exception:
            return False
