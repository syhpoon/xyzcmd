#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
#

class MultiParser(BaseParser):
    """
    MultiParser is a simple container for any other parsers
    Usually parsers, such as BlockParser designed to parse homogeneous blocks in
    single source: file or string. But still it might be useful sometimes to
    parse multiple blocks of different syntax in single source.
    Thus, one can register few necessary parser into MultiParser and go on.
    """

    def __init__(self):
        pass
