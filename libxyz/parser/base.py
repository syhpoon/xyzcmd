#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
#

"""
Provides BaseParser class.
"""

class BaseParser(object):
    """
    Parent class for all parsers in libxyz
    """

    def __init__(self):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def parse(self):
        """
        Do actual parsing
        """

        raise NotImplementedError(_("Method not implemented"))
