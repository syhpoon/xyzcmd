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

import re

from libxyz.parser import BaseParser
from libxyz.parser import Lexer
from libxyz.parser import ParsedData
from libxyz.exceptions import XYZValueError
from libxyz.exceptions import LexerError

class BlockParser(BaseParser):
    """
    BaseParser is used to parse block structures.
    Format:

    name {
        var1 <assign> val1 <delimiter>
        var2 <assign> val2 [<list_separator>val3...] <delimiter>
        ...
        }
    """

    STATE_INIT = 0
    STATE_BLOCK_OPEN = 1
    STATE_VARIABLE = 2
    STATE_ASSIGN = 3
    STATE_VALUE = 4
    STATE_DELIM = 5
    STATE_LIST_VALUE = 6

    DEFAULT_OPT = {
                   u"comment": u"#",
                   u"varre": re.compile(r"^[\w-]+$"),
                   u"assignchar": u"=",
                   u"delimiter": u"\n",
                   u"validvars": (),
                   u"value_validator": None,
                   u"count": 0,
                   u"list_separator": u",",
                   u"macrochar": u"&",
                   }

    def __init__(self, opt=None, default_data=None):
        """
        @param opt: Parser options.
        @type opt: dict

        Available options:
            - comment: Comment character.
              Everything else ignored until EOL.
              Type: I{string (single char)}
              Default: #
            - delimiter: Character to use as delimiter between statements.
              Type: I{string (single char)}
              Default: \\n
            - varre: Valid variable name regular expression.
              Type: I{Compiled re object (L{re.compile})}
              Default: ^[\w-]+$
            - assignchar: Variable-value split character.
              Type: I{string (single char)}
              Default: =
            - validvars: List of variables valid within block.
              Type: I{sequence}
              Default: ()
            - value_validator: Value validator
              Type: A function that takes three args:
              current block, var and value and validates them.
              In case value is invalid, XYZValueError must be raised.
              Otherwise function must return required value, possibly modified.
              Default: None
            - count: How many blocks to parse. If count <= 0 - will parse
              all available.
              Type: integer
              Default: 0
            - list_separator: Character to separate elements in list
              Type: I{string (single char)}
              Default: ,
            - macrochar: Macro character (None to disable macros)
              Type: I{string (single char)}
              Default: &

        @param default_data: Dictionary containing L{libxyz.parser.ParsedData}
                             objects with default values.
        """

        super(BlockParser, self).__init__()

        if opt and not isinstance(opt, dict):
            raise XYZValueError(_(u"Invalid opt type: %s. "\
                                  u"Dictionary expected." % type(opt)))

        self.opt = opt or self.DEFAULT_OPT
        self.set_opt(self.DEFAULT_OPT, self.opt)

        self._default_data = default_data
        self._state = self.STATE_INIT
        self._parsed_obj = None
        self._varname = None
        self._macroname = None
        self._sdata = None
        self._result = {}
        self._current_list = []
        self._macros = {}
        self._lexer = None
        self._openblock = u"{"
        self._closeblock = u"}"

        self._tok_type = None

        self._parse_table = {
            self.STATE_INIT: self._process_state_init,
            self.STATE_BLOCK_OPEN: self._process_state_block_open,
            self.STATE_VARIABLE: self._process_state_variable,
            self.STATE_ASSIGN: self._process_state_assign,
            self.STATE_VALUE: self._process_state_value,
            self.STATE_LIST_VALUE: self._process_state_list_value,
            self.STATE_DELIM: self._process_state_delim,
            }

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def parse(self, source):
        """
        Parse blocks of text and return a dict of L{ParsedData} objects
        or raise L{libxyz.exceptions.ParseError} exception

        @param source: Source data
        """

        self._result = {}

        self._cleanup()

        _tokens = (self._openblock,
                   self._closeblock,
                   self.assignchar,
                   self.delimiter,
                   self.list_separator,
                  )

        self._lexer = Lexer(source, _tokens, self.comment, self.macrochar)
        self._sdata = self._lexer.sdata

        try:
            while True:
                _res = self._lexer.lexer()

                if _res is None:
                    break
                else:
                    self._tok_type, _val = _res

                # We're only interested in LF in DELIM or LIST_VALUE
                # states
                if _val == "\n" and \
                self._state not in (self.STATE_DELIM, self.STATE_LIST_VALUE):
                    continue
                else:
                    self._parse_table[self._state](_val)
        except LexerError, e:
            self.error(str(e))

        self._check_complete()

        return self._result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _process_state_init(self, word):
        if self._default_data and word in self._default_data:
            self._parsed_obj = self._default_data[word]
        else:
            self._parsed_obj = ParsedData(word)

        self._state = self.STATE_BLOCK_OPEN

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _process_state_block_open(self, word):
        if word != self._openblock:
            self.error(msg=(word, self._openblock),
                       etype=self.error_unexpected)
        else:
            self._state = self.STATE_VARIABLE

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _process_state_variable(self, word):
        if word == self._closeblock:
            self._complete_block()
            return

        if self._tok_type == self._lexer.TOKEN_MACRO:
            self._macroname = word
        else:
            if self.validvars and word not in self.validvars:
                self.error(_(u"Unknown variable %s" % word))
            elif self.varre.match(word) is None:
                self.error(_(u"Invalid variable name: %s" % word))

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

    def _process_state_list_value(self, word):
        if word == self.list_separator:
            self._state = self.STATE_VALUE
            return

        if len(self._current_list) == 1:
            _value = self._current_list[0]
        else:
            _value = tuple(self._current_list)

        # Macro
        if self._macroname:
            self._macros[self._macroname] = _value
            self._macroname = None
        # Variable
        else:
            if self.value_validator:
                try:
                    _value = self.value_validator(self._parsed_obj.name,
                                                  self._varname, _value)
                except XYZValueError, e:
                    self.error(_(u"Invalid value: %s" % str(e)))

            self._parsed_obj[self._varname] = _value
            self._varname = None

        self._current_list = []
        self._lexer.escaping_off()
        self._state = self.STATE_DELIM
        self._lexer.unget(word)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _process_state_value(self, word):
        if self._tok_type == self._lexer.TOKEN_MACRO:
            try:
                self._current_list.append(self._macros[word])
            except KeyError:
                self.error(_(u"Undefined macro %s" % word))
        else:
            self._current_list.append(word)

        self._state = self.STATE_LIST_VALUE

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _process_state_delim(self, word):
        if word == self._closeblock:
            self._complete_block()
            return
        if word != self.delimiter:
            self.error(msg=(word, self.delimiter),
                        etype=self.error_unexpected)
        else:
            self._state = self.STATE_VARIABLE

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _complete_block(self):
        if self._parsed_obj:
            self._result[self._parsed_obj.name] = self._parsed_obj

        self._cleanup()

        if self.count > 0 and self.count == len(self._result):
            self._lexer.done()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _cleanup(self):
        """
        Set all neccessary variables to initial state
        """

        self._parsed_obj = None
        self._varname = None
        self._macroname = None
        self._state = self.STATE_INIT
        self._in_comment = False
        self._in_quote = False
        self._current_list = []
        self._macros = {}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _check_complete(self):
        """
        Check state after source reaches EOF for consistency
        """

        _err = False
        _msg = None

        if self._in_quote:
            _err, _msg = True, _(u"Unterminated quote")

        if self._state != self.STATE_INIT:
            if self._state != self.STATE_BLOCK_OPEN:
                _err, _msg = True, _(u"Unclosed block")
            else:
                _err, _msg = True, None

        if self._lexer.get_idt():
            _err, _msg = True, None

        if _err:
            self.error(_msg)
