#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
#

import types

class SourceData(object):
    """
    Source data iterator class
    """

    FILE = 0
    STRING = 1

    def __init__(self, source):
        """
        @param source: Source
        @type source: String or file-like object
        """

        self.lineno = 1

        self._source = None
        self._index = 0
        self._next_me = None
        self._len = 0
        self._buffer = []

        self._source = source

        if type(source) in types.StringTypes:
            self._type = self.STRING
            self._next_me = self._next_string
            self._len = len(self._source)
        else:
            self._type = self.FILE
            self._next_me = self._next_file

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __iter__(self):
        return self

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def next(self):
        _res = None

        if self._buffer:
            _res = self._buffer.pop()
        else:
            _res = self._next_me()

        if _res == "\n":
            self.lineno += 1

        return _res

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _next_file(self):
        _char = self._source.read(1)

        # EOF
        if not _char:
            raise StopIteration()
        else:
            return _char

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _next_string(self):
        if self._index >= self._len:
            raise StopIteration()
        else:
            _char = self._source[self._index]
            self._index += 1
            return _char

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def unget(self, string):
        """
        Put token back onto input stream
        """

        self._buffer.extend(reversed(string))
