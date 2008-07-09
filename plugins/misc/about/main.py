#-*- coding: utf8 -*
#
# Max E. Kuznecov <syhpoon@syhpoon.name> 2008
#

from libxyz.core.plugins import BasePlugin

class XYZPlugin(BasePlugin):
    "Plugin about"

    NAME = u"about"
    AUTHOR = u"Max E. Kuznecov <syhpoon@syhpoon.name>"
    VERSION = u"0.1"
    BRIEF_DESCRIPTION = u"About plugin"
    FULL_DESCRIPTION = u""
    NAMESPACE = u"misc"
    MIN_XYZ_VERSION = None
    DOC = None
    HOMEPAGE = None

    def __init__(self, xyz):
        super(XYZPlugin, self).__init__(xyz)

        self.public = {}
