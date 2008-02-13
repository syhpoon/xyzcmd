#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
#

"""
BlockParser parses block of configration
"""

import re
import types

from libxyz.parser import BaseParser, ParsedData, SourceData
from libxyz.exceptions import XYZValueError

class BlockParser(BaseParser):
    """
    BaseParser is used to parse blocked structures
    Format:

    name {
        var1 <assign> val1 <delimiter>
        var2 <assign> val2 [,val3,...] <delimiter>
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
                   "comment": "#",
                   "varre": re.compile(r"^[\w-]+$"),
                   "assignchar": "=",
                   "delimiter": "\n",
                   "validvars": (),
                   "value_validator": None,
                   "count": 0,
                   "list_separator": ",",
                   }

    def __init__(self, opt=None):
        """
        @param opt: Parser options.
        @type opt: dict

        Available options:
            - comment: Comment character.
              Everything else ignored until EOL.
              Type: I{string (single char)}
            - delimiter: Character to use as delimiter between statements.
              Type: I{string (single char)}
            - varre: Valid variable name regular expression.
              ^[\w-]+$ re is used unless given.
              Type: I{Compiled re object (L{re.compile})}
            - assignchar: Variable-value split character.
              Type: I{string (single char)}
            - delimiter: Character that terminates statement.
              Type: I{string}
            - validvars: List of variables valid within block.
              Type: I{sequence}
            - value_validator: Value validator
              Type: A function that takes two args var and value
              and validates them. In case value is invalid,
              ValueError must be raised. Otherwise returning
              True is sufficient.
            - count: How many blocks to parse. If count < 1 - will parse
              all available.
              Type: integer
            - list_separator: Character to separate elements in list
              Type: I{string (single char)}
        """

        super(BlockParser, self).__init__()

        if opt and type(opt) != types.DictType:
            raise XYZValueError(_("Invalid opt type: %s. "\
                                  "Dictionary expected." % type(opt)))

        self.opt = opt or self.DEFAULT_OPT

        for _opt in self.DEFAULT_OPT.keys():
            setattr(self, _opt, self.opt.get(_opt, self.DEFAULT_OPT[_opt]))

        self._state = self.STATE_INIT
        self._parsed_obj = None
        self._varname = None
        self._sdata = None
        self._result = {}
        self._current_list = []

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
        Parse block of text and return L{ParsedData} object or raise
        L{libxyz.exceptions.ParseError} exception

        @param source: Parsing source. If file object is passed, it must be
                       closed by caller function after parsing completes.
        @type block: string, file-like object or SourceData object

        @return: List of L{libxyz.parser.ParsedData} parsed objects
        """

        self._result = {}

        self._cleanup()

        if isinstance(source, SourceData):
            self._sdata = source
        else:
            self._sdata = SourceData(source)

        _tokens = ("{", "}",
                   self.assignchar,
                   self.delimiter,
                   self.list_separator,
                  )

        for _lex, _val in self.lexer(self._sdata, _tokens, self.comment):
            # We're only interested in LF in DELIM or LIST_VALUE
            # states
            if _val == "\n" and \
               self._state not in (self.STATE_DELIM, self.STATE_LIST_VALUE):
                continue
            else:
                self._parse_table[self._state](_val)

        self._check_complete()

        return self._result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _process_state_init(self, word):
        self._parsed_obj = ParsedData(word)
        self._state = self.STATE_BLOCK_OPEN

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _process_state_block_open(self, word):
        if word != "{":
            self.error(msg=(word, "{"), etype=self.error_unexpected)
        else:
            self._state = self.STATE_VARIABLE

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _process_state_variable(self, word):
        if word == "}":
            # Closing block
            if self._parsed_obj:
                self._result[self._parsed_obj.name] = self._parsed_obj
            self._cleanup()

            if self.count > 0 and self.count == len(self._result):
                self._done = True
            return
        if self.validvars and word not in self.validvars:
                self.error(_("Unknown variable %s" % word))
        elif self.varre.match(word) is None:
            self.error(_("Invalid variable name: %s" % word))

        self._varname = word
        self._state = self.STATE_ASSIGN

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _process_state_assign(self, word):
        if word != self.assignchar:
            self.error(msg=(word, self.assignchar),
                       etype=self.error_unexpected)
        else:
            self._state = self.STATE_VALUE
            self._can_escape = True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _process_state_list_value(self, word):
        if word == self.list_separator:
            self._state = self.STATE_VALUE
            return

        # Else combine value
        if self.value_validator:
            try:
                for _el in self._current_list:
                    self.value_validator(self._varname, _el)
            except ValueError, e:
                self.error(_("Invalid value %s: %s" % (_el, str(e))))

        if len(self._current_list) == 1:
            _value = self._current_list[0]
        else:
            _value = tuple(self._current_list)

        self._current_list = []

        self._parsed_obj[self._varname] = _value
        self._varname = None
        self._can_escape = False
        self._state = self.STATE_DELIM
        self._sdata.unget(word)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _process_state_value(self, word):
        self._current_list.append(word)
        self._state = self.STATE_LIST_VALUE

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _process_state_delim(self, word):
        if word == "}":
            if self._parsed_obj:
                self._result[self._parsed_obj.name] = self._parsed_obj
            self._cleanup()

            if self.count > 0 and self.count == len(self._result):
                self._done = True
            return
        if word != self.delimiter:
            self.error(msg=(word, self.delimiter),
                        etype=self.error_unexpected)
        else:
            self._state = self.STATE_VARIABLE

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _cleanup(self):
        """
        Set all neccessary variables to initial state
        """

        self._done = False
        self._parsed_obj = None
        self._sdata = None
        self._varname = None
        self._state = self.STATE_INIT
        self._in_comment = False
        self._in_quote = False
        self._current_list = []

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _check_complete(self):
        """
        Check state after source reaches EOF for consistency
        """

        _err = False
        _msg = None

        if self._in_quote:
            _err, _msg = True, _("Unterminated quote")

        if self._state != self.STATE_INIT:
            if self._state != self.STATE_BLOCK_OPEN:
                _err, _msg = True, _("Unclosed block")
            else:
                _err, _msg = True, None

        if self.get_idt():
            _err, _msg = True, None

        if _err:
            self.error(_msg)
