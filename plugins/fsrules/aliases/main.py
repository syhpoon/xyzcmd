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
    "Aliases for FSRule"

    NAME = u"aliases"
    AUTHOR = u"Max E. Kuznecov <mek@mek.uz.ua>"
    VERSION = u"0.1"
    BRIEF_DESCRIPTION = _(u"FSRule aliases")
    FULL_DESCRIPTION = _(u"Plugin provides some useful FSRule aliases")
    NAMESPACE = u"fsrules"
    MIN_XYZ_VERSION = None
    DOC = _(
        u"Available aliases:\n"\
        u"file_or_link: Matches file objects or links to file objects.\n"\
        u"dir_or_link: Matches directory objects or links to directory objects"
        )
    HOMEPAGE = "http://xyzcmd.syhpoon.name"

    def __init__(self, xyz):
        super(XYZPlugin, self).__init__(xyz)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def prepare(self):
        FSRule.extend("file_or_link", self._transform, self._file_or_link)
        FSRule.extend("dir_or_link", self._transform, self._dir_obr_link)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def finalize(self):
        FSRule.unextend("file_or_link")
        FSRule.unextend("dir_or_link")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _transform(self, arg):
        """
        Transformation stub
        """

        return None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _file_or_link(self, vfsobj, _):
        return vfsobj.is_file() or \
               (vfsobj.is_link() and vfsobj.data.is_file())

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def _dir_or_link(self, vfsobj, _):
        return vfsobj.is_dir() or \
               (vfsobj.is_link() and vfsobj.data.is_dir())
