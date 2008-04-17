#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
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

from libxyz.parser import BaseParser
from libxyz.parser import SourceData
from libxyz.exceptions import XYZValueError
from libxyz.exceptions import ParseError

class RegexpParser(BaseParser):
    """
    RegexpParser is used to parse statements based on regular expressions
    It is only useful for parsing linear, non-structured files.
    """

    def __init__(self, cbpool):
        """
        @param cbpool: Dictionary with compiled regexp as keys and
                       callback functions as values.
                       Upon matching regexp, callback will be called with
                       MatchObject as an argument. Callback function should
                       raise XYZValueError in case of any error and True
                       otherwise.
        """

        super(RegexpParser, self).__init__()

        self.cbpool = cbpool
        self.sfile = None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def parse(self, source):
        """
        Parse config
        """

        self.sfile = None
        _lineno = 1
        _source = self.get_source(source)

        for _line in _source:
            for _regexp in self.cbpool:
                _res = _regexp.search(_line.strip())

                if _res is not None:
                    try:
                        self.cbpool[_regexp](_res)
                    except XYZValueError, e:
                        raise ParseError(_(u"Parse erorr on line %d: %s"\
                                         % (_lineno, e)))
                    else:
                        _lineno += 1

        if self.sfile is not None:
            self.sfile.close()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_source(self, source):
        """
        Determine type of the source
        """

        _src = None

        if isinstance(source, basestring):
            # List of lines
            _src = source.splitlines(True)
        else:
            try:
                self.sfile = open(source, "r")
            except IOError, e:
                raise ParseError(_(u"Unable to open file %s for reading: %s"\
                                 % (source, unicode(e))))
            else:
                _src = self.sfile

        return _src
