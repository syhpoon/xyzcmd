#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <syhpoon@syhpoon.name> 2008
#

from libxyz.core.plugins import BasePlugin
from libxyz.ui import MessageBox
from libxyz.version import Version

class XYZPlugin(BasePlugin):
    """
    Example plugin
    """

    # Plugin name
    NAME = u"hello"

    # AUTHOR: Author name
    AUTHOR = u"Max E. Kuznecov ~syhpoon <syhpoon@syhpoon.name>"

    # VERSION: Plugin version
    VERSION = u"0.1"

    # Brief one line description
    BRIEF_DESCRIPTION = u"Simple hello plugin"

    # Full plugin description
    FULL_DESCRIPTION = u"""\
Hello plugin is an example of XYZCommander plugin.
It shows main aspects of plugin creation.
Functionality is limited to single method: say_hello
which shows greeting message box.\
"""

    # NAMESPACE: Plugin namespace. For detailed information about
    #            namespaces see Plugins chapter of XYZCommander user manual.
    #            Full namespace path to method is:
    #            xyz:plugins:misc:hello:SayHello

    NAMESPACE = "misc"

    def __init__(self, xyz):
        super(XYZPlugin, self).__init__(xyz)

        self.export(self.say_hello)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def prepare(self):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def finalize(self):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def say_hello(self):
        """
        Shows simple greeting dialog
        """

        _msg = self.FULL_DESCRIPTION
        _dim = self.xyz.screen.get_cols_rows()
        _title = u"XYZCommander version %s" % Version.version

        _box = MessageBox(self.xyz, self.xyz.top, _msg, _title)

        return _box.show()
