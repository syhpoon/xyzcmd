#-*- coding: utf8 -*
#
# Max E. Kuznecov <syhpoon@syhpoon.name> 2009
#

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

    FULL_DESCRIPTION = u""
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
