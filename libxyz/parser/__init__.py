#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
#

"""
Different parsers
"""

__all__ = ('BaseParser',
           'BlockParser',
           'MultiParser',
           'ParsedData',
)

from base import BaseParser, ParsedData
from block import BlockParser
from multi import MultiParser
