#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
#

class ParsedData(object):
    """
    Parsed data
    Provides dictionary-like access to parsed values
    """

    def __init__(self, name=None):
        self.name = name
        self._data = {}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __str__(self):
        return "ParsedData object: %s" % str(self._data)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __repr(self):
        return __str__()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __getitem__(self, var):
        return self.lookup(var)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __setitem__(self, var, val):
        self.set(var, val)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def lookup(self, var):
        """
        Lookup for value of variable
        If variable does not exist, return None
        """

        if var in self._data:
            return self._data[var]
        else:
            raise KeyError()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def set(self, var, val):
        """
        Set new value to variable
        """

        self._data[var] = val
