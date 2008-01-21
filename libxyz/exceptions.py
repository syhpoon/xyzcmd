#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
#

class XYZError(Exception):
    """
    Base exception
    """

    pass

#++++++++++++++++++++++++++++++++++++++++++++++++

class ParseError(XYZError):
    """
    Parsing error
    """

    pass

#++++++++++++++++++++++++++++++++++++++++++++++++

class PluginError(XYZError):
    """
    Plugin error
    """

    pass
