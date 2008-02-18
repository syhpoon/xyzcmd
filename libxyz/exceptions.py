#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
#

class XYZError(Exception):
    """
    Base exception
    """

    pass

#++++++++++++++++++++++++++++++++++++++++++++++++

class XYZRuntimeError(XYZError):
    pass

#++++++++++++++++++++++++++++++++++++++++++++++++

class XYZValueError(XYZError):
    pass

#++++++++++++++++++++++++++++++++++++++++++++++++

class ParseError(XYZError):
    pass

#++++++++++++++++++++++++++++++++++++++++++++++++

class LexerError(XYZError):
    pass

#++++++++++++++++++++++++++++++++++++++++++++++++

class PluginError(XYZError):
    pass
