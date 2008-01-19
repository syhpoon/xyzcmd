#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
#

"""
BlockParser parses one block of configration
"""

from libxyz.parser import BaseParser

class BlockParser(BaseParser):
    """
    BaseParser used to parse onew block of configration
    Format:

    block [name] {
        var1 = val1 [delimiter]
        var2 = val2 [delimiter]
        ...
        }
    """

    def __init__(self):
        super(BlockParser, self).__init__()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def parse(self, block):
        """
        Parse block of text and return L{ParsedData} object or raise
        L{ParseError} exception

        @param block: Text to parse
        @type block: string

        @return: L{ParsedData} parsed object
        """

        pass
