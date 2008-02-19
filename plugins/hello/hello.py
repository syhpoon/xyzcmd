#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
#

from libxyz.core.plugin import BasePlugin

class Hello(BasePlugin):
    """
    Example plugin
    """

    def __init__(self):
        self.public["SayHello"] = self._say_hello

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _say_hello(self):
        """
        Exported method
        Shows simple greeting dialog
        """

        print "HELLO!"
