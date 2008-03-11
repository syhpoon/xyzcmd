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

import types
import re

from libxyz.parser import Lexer
from libxyz.parser import BaseParser
from libxyz.parser import SourceData
from libxyz.exceptions import XYZValueError
from libxyz.exceptions import LexerError
from libxyz.exceptions import ParseError

class MultiParser(BaseParser):
    """
    MultiParser is a simple container for any other parsers
    Usually parsers, such as BlockParser designed to parse homogeneous blocks in
    single source: file or string. But still it might be useful sometimes to
    parse multiple blocks of different syntax in single source.
    Thus, one can register some necessary parsers into MultiParser and go on.
    """

    DEFAULT_OPT = {
                   u"comment": u"#",
                   u"tokens": (),
                   }

    def __init__(self, parsers, opt=None):
        """
        @param parsers: dictionary containing string, list or
                        compiled regexp of keywords as key
                        and *Parser object as value.
        @type parsers: dictionary with string or sequence keys

        @param opt: Options

        Available options:
        - comment: Comment character.
          Everything else ignored until EOL.
          Type: I{string (single char)}

        - tokens: List of tokens.
          Type: I{sequence}
        """

        super(MultiParser, self).__init__()

        self._rx = re.compile("")

        if parsers:
            if type(parsers) != types.DictType:
                raise XYZValueError(_(u"Invalid argument type %s. "\
                                      u"Dictionary expected" % str(parsers)))
            else:
                self.parsers = parsers
        else:
            self.parsers = {}

        self.opt = opt or self.DEFAULT_OPT
        self.set_opt(self.DEFAULT_OPT, self.opt)

        self._lexer = None
        self._result = {}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def parse(self, source):
        """
        Begin parsing
        """

        def _get_parser(val):
            _p = None

            for _key in self.parsers:
                if type(_key) in types.StringTypes and _key == val:
                    _p = self.parsers[_key]
                    break
                elif type(_key) == type(self._rx) and _key.match(val):
                    _p = self.parsers[_key]
                    break
                elif hasattr(_key, "__contains__") and val in _key:
                    _p = self.parsers[_key]
                    break

            return _p

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self._result = {}
        self._lexer = Lexer(source, self.tokens, self.comment)

        try:
            while True:
                _res = self._lexer.lexer()

                if _res is None:
                    break
                else:
                    _lex, _val = _res

                _parser = _get_parser(_val)

                if _parser:
                    # Push read token back
                    self._lexer.unget(_val)
                    self._result.update(_parser.parse(self._lexer.sdata))
                else:
                    self.error(_(u"Unknown keyword: %s" % _val))
        except LexerError, e:
            self.error(str(e))

        return self._result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def register(self, keyword, parser):
        """
        Register new parser. If parser for keyword given already registered
        replace it with new one.

        @param keyword: Keyword that will trigger the parser.
        @type keyword: string

        @param param: Any *Parser instance. Must be subclassed
                      from L{BaseParser}.
        """

        if not isinstance(parser, BaseParser):
            raise XYZValueError(_(u"Invalid argument type %s. "\
                                  u"BaseParser or subclassed expected" % \
                                  str(parsers)))

        self.parsers[keyword] = parser

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def unregister(self, keyword):
        """
        Unregister parser. Ignore if was not registered.
        """

        try:
            del(self.parsers[keyword])
        except KeyError:
            pass
