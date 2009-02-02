#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <syhpoon@syhpoon.name> 2008
#
# This file is part of XYZCommander.
# XYZCommander is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# XYZCommander is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser Public License for more details.
# You should have received a copy of the GNU Lesser Public License
# along with XYZCommander. If not, see <http://www.gnu.org/licenses/>.

import libxyz

class SourceData(object):
    """
    Source data iterator class
    """

    FILE = 0
    STRING = 1

    def __init__(self, source, bytes=True):
        """
        @param source: Source
        @type source: String or file-like object
        @param bytes: If True then object will produce single byte on iteration
                      Otherwise it will be single line.
        """

        self.lineno = 1

        self._bytes = bytes
        self._source = None
        self._index = 0
        self._next_me = None
        self._len = 0
        self._buffer = []

        self._source = source
        self._intern = u""

        if isinstance(source, basestring):
            self._intern = _(u"Source string")
            self._type = self.STRING
            self._next_me = self._next_string
            self._len = len(self._source)
        # Open file-like object supposed
        else:
            self._intern = libxyz.core.utils.ustring(source.name)
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

        _res = libxyz.core.utils.ustring(_res)

        if _res == u"\n":
            self.lineno += 1

        return _res

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _next_file(self):
        if self._bytes:
            _data = self._source.read(1)
        else:
            _data = self._source.readline()

        # EOF
        if not _data:
            raise StopIteration()
        else:
            return _data

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _next_string(self):
        if self._index >= self._len:
            raise StopIteration()

        if not self._bytes:
            _nl = self._source.find(u"\n")

            if _nl == -1:
                _data = self._source[self._index:]
                self._index = len(_data)
            else:
                _data = self._source[self._index:_nl]
                self._index = _nl
        else:
            _data = self._source[self._index]
            self._index += 1

        return _data

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def unget(self, string):
        """
        Put token back onto input stream
        """

        self._buffer.extend(reversed(string))

        # Decrease lineno if needed
        self.lineno -= string.count(u"\n")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def desc(self):
        """
        Get source data description
        """

        return self._intern
