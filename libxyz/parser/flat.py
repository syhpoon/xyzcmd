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

from libxyz.parser import Lexer
from libxyz.parser import BaseParser
from libxyz.exceptions import XYZValueError
from libxyz.exceptions import ParseError
from libxyz.exceptions import LexerError

class FlatParser(BaseParser):
    """
    FlatParser is simple linear parser.

    Format:

    var1 <assign> val1 <delimiter>
    var2 <assign> val2 <delimiter>
    ...
    """

    STATE_VARIABLE = 0
    STATE_ASSIGN = 1
    STATE_VALUE = 2
    STATE_DELIM = 3

    DEFAULT_OPT = {
                   "comment": "#",
                   "assignchar": ":",
                   "delimiter": "\n",
                   "count": 0,
                   }

    def __init__(self, opt=None):
        """
        @param opt: Options
        @type opt: dict

        Available options:
            - comment: Comment character.
              Everything else ignored until EOL.
              Type: I{string (single char)}
            - assignchar: Variable-value split character.
              Type: I{string (single char)}
            - delimiter: Character to use as delimiter between statements.
              Type: I{string (single char)}
        """

        super(FlatParser, self).__init__()

        self._lexer = None

        self.opt = opt or self.DEFAULT_OPT
        self.set_opt(self.DEFAULT_OPT, self.opt)

        self._cleanup()

        self._parse_table = {
            self.STATE_VARIABLE: self._process_state_variable,
            self.STATE_ASSIGN: self._process_state_assign,
            self.STATE_VALUE: self._process_state_value,
            self.STATE_DELIM: self._process_state_delim,
        }

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def parse(self, source):
        """
        Begin parsing
        """

        self._cleanup()

        _tokens = (self.assignchar, self.delimiter)
        self._lexer = Lexer(source, _tokens, self.comment)

        try:
            while True:
                _res = self._lexer.lexer()

                if _res is None:
                    break
                else:
                    _lex, _val = _res

                if _val == "\n" and self._state != self.STATE_DELIM:
                    continue
                self._parse_table[self._state](_val)
        except LexerError, e:
            self.error(str(e))

        self._check_complete()

        return self._result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _process_state_variable(self, word):
        if self.count > 0 and self.count == len(self._result):
            self._lexer.done()
            return

        self._varname = word
        self._state = self.STATE_ASSIGN

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _process_state_assign(self, word):
        if word != self.assignchar:
            self.error(msg=(word, self.assignchar),
                       etype=self.error_unexpected)
        else:
            self._state = self.STATE_VALUE
            self._lexer.escaping_on()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _process_state_value(self, word):
        self._result[self._varname] = word
        self._varname = None
        self._lexer.escaping_off()
        self._state = self.STATE_DELIM

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _process_state_delim(self, word):
        if self.count > 0 and self.count == len(self._result):
            self._lexer.done()
            return

        if word != self.delimiter:
            self.error(msg=(word, self.delimiter),
                       etype=self.error_unexpected)
        else:
            self._state = self.STATE_VARIABLE

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _cleanup(self):
        self._result = {}
        self._state = self.STATE_VARIABLE
        self._varname = None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _check_complete(self):
        if self._state not in (self.STATE_VARIABLE, self.STATE_DELIM):
            self.error(_("Unterminated expression"))
