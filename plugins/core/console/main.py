#-*- coding: utf8 -*
#
# Max E. Kuznecov <mek@mek.uz.ua> 2008
#

from libxyz.core.plugins import BasePlugin

class XYZPlugin(BasePlugin):
    "Plugin console"

    # Plugin name
    NAME = u"console"

    # AUTHOR: Author name
    AUTHOR = u"Max E. Kuznecov <mek@mek.uz.ua>"

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

    NAMESPACE = u"core"

    def __init__(self, xyz):
        super(XYZPlugin, self).__init__(xyz)

        self.public = {}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def prepare(self):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def finalize(self):
        pass

