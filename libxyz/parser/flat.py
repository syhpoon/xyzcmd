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

from libxyz.parser import Lexer
from libxyz.parser import BaseParser
from libxyz.parser import ParsedData

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
    STATE_LIST_VALUE = 3
    STATE_DELIM = 4

    DEFAULT_OPT = {
                   u"comment": u"#",
                   u"assignchar": u":",
                   u"delimiter": u"\n",
                   u"validvars": (),
                   u"value_validator": None,
                   u"count": 0,
                   u"list_separator": u",",
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
            - validvars: List of variables valid within block.
              Type: I{sequence}
            - value_validator: Value validator
              Type: A function that takes two args:
              variable and value and validates them.
              In case value is invalid, XYZValueError must be raised.
              Otherwise function must return required value, possibly modified.
            - count: How many blocks to parse. If count <= 0 - will parse
              all available.
              Type: integer
            - list_separator: Character to separate elements in list
              Type: I{string (single char)}
              Default: ,
        """

        super(FlatParser, self).__init__()

        self._parsed = 0
        self._result = ParsedData()
        self._current_list = []
        self._lexer = None
        self._state = self.STATE_VARIABLE

        self.opt = opt or self.DEFAULT_OPT
        self.set_opt(self.DEFAULT_OPT, self.opt)

        self._parse_table = {
            self.STATE_VARIABLE: self._process_state_variable,
            self.STATE_ASSIGN: self._process_state_assign,
            self.STATE_VALUE: self._process_state_value,
            self.STATE_LIST_VALUE: self._process_state_list_value,
            self.STATE_DELIM: self._process_state_delim,
        }

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def parse(self, source, default_data=None):
        """
        Begin parsing
        @param default_data: Dictionary with default values.
        """

        self._cleanup()

        if default_data and isinstance(default_data, dict):
            self._result = default_data.copy()

        _tokens = (
                   self.assignchar,
                   self.delimiter,
                   self.list_separator
                  )

        self._lexer = Lexer(source, _tokens, self.comment, macro=None)

        try:
            while True:
                _res = self._lexer.lexer()

                if _res is None:
                    break
                else:
                    _lex, _val = _res

                if _val == u"\n" and self._state not in \
                (self.STATE_DELIM, self.STATE_LIST_VALUE):
                    continue
                self._parse_table[self._state](_val)
        except LexerError, e:
            self.error(str(e))

        # Finish assembling value
        if self._state == self.STATE_LIST_VALUE:
            self._process_state_list_value(None)

        self._check_complete()

        return self._result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _process_state_variable(self, word):
        if self.count > 0 and self.count == self._parsed:
            self._lexer.done()
            return

        if self.validvars and word not in self.validvars:
                self.error(_(u"Unknown variable %s" % word))
        else:
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
        self._current_list.append(word)
        self._state = self.STATE_LIST_VALUE

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _process_state_list_value(self, word):
        if word == self.list_separator:
            self._state = self.STATE_VALUE
            return

        if len(self._current_list) == 1:
            _value = self._current_list[0]
        else:
            _value = tuple(self._current_list)

        if self.value_validator:
            try:
                _value = self.value_validator(self._varname, _value)
            except XYZValueError, e:
                self.error(_(u"Invalid value: %s" % str(e)))

        self._result[self._varname] = _value
        self._parsed += 1
        self._varname = None

        self._current_list = []
        self._lexer.escaping_off()
        self._state = self.STATE_DELIM

        if word is not None:
            self._lexer.unget(word)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _process_state_delim(self, word):
        if self.count > 0 and self.count == self._parsed:
            self._lexer.done()
            return

        if word != self.delimiter:
            self.error(msg=(word, self.delimiter),
                       etype=self.error_unexpected)
        else:
            self._state = self.STATE_VARIABLE

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _cleanup(self):
        self._parsed = 0
        self._state = self.STATE_VARIABLE
        self._varname = None
        self._result = ParsedData()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _check_complete(self):
        if self._state not in (self.STATE_VARIABLE, self.STATE_DELIM):
            self.error(_(u"Unterminated expression"))
