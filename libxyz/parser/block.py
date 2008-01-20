#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
#

"""
BlockParser parses one block of configration
"""

import types
import re

from libxyz.exceptions import ParseError

class BlockParser(object):
    """
    BaseParser used to parse blocked structures
    Format:

    block [name] {
        var1 = val1
        var2 = val2
        ...
        }
    """

    STATE_INIT = 0
    STATE_NAME_OR_OPEN = 1
    STATE_BLOCK_OPEN = 2
    STATE_VARIABLE = 3
    STATE_ASSIGN = 4
    STATE_VALUE = 5

    error_unexpected = 1

    def __init__(self, keyword, has_name=False, comment="#", varre=None,
                 assignchar="=", validvars=None):
        """
        @param keyword: Word that indicates block start
        @type keyword: string

        @param has_name: Does block has name
        @type has_name: boolean

        @param has_name: Does block has name
        @type has_name: boolean

        @param delimiter: Character to use as delimiter between statements
        @type delimiter: string

        @param comment: Comment character. Everything else ignored until EOL
                        if found.
        @type comment: string (single char)

        @param varre: Valid variable name regular expression,
                      ^[\w-]+$ re is used unless given.
        @type varre: Compiled re object (L{re.compile})

        @param assignchar: Variable-value split character.
        @type assignchar: string (single char)

        @param validvars: List of variables valid within block
        @type delimiter: sequence

        """

        self.keyword = keyword
        self.has_name = has_name
        self.comment = comment
        self.varre = varre or re.compile(r"^[\w-]+$")
        self.assignchar = assignchar
        self.validvars = validvars or ()

        self._lineno = 0
        self._state = self.STATE_INIT
        self._parsed_obj = None
        self._varname = None
        self._result = []
        self._in_comment = False
        self._in_quote = False

        self._parse_table = {
            self.STATE_INIT: self._process_state_init,
            self.STATE_NAME_OR_OPEN: self._process_state_name_or_open,
            self.STATE_BLOCK_OPEN: self._process_state_block_open,
            self.STATE_VARIABLE: self._process_state_variable,
            self.STATE_ASSIGN: self._process_state_assign,
            self.STATE_VALUE: self._process_state_value,
            }

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def parse(self, source):
        """
        Parse block of text and return L{ParsedData} object or raise
        L{ParseError} exception

        @param source: Parsing source
        @type block: string or file-like object

        @return: List of L{ParsedBlockData} parsed objects
        """

        def _put_token(token):
            self._parse_table[self._state](token)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self._lineno = 1
        self._result = []

        self._cleanup()

        _tokens = ("{", "}", self.assignchar)

        # sdata must be a list of lines
        if type(source) in types.StringTypes:
            sdata = source.splitlines(True)
        else:
            sdata = source

        idt = []
        quote = []

        for line in sdata:
            for char in line:
                if char == "\n":
                    if self._in_quote:
                        self._error(_("Unterminated quote"))
                    elif idt:
                        _put_token("".join(idt))
                        idt = []
                    self._in_comment = False
                    self._lineno += 1
                    continue

                if self._in_comment:
                    continue

                if char == '"':
                    if self._in_quote:
                        self._in_quote = False
                        _put_token("".join(quote))
                    else:
                        self._in_quote = True

                    quote = []
                    continue

                if self._in_quote:
                    quote.append(char)
                    continue

                if char in _tokens:
                    # Check if we finished assembling a word
                    if idt:
                        _put_token("".join(idt))
                        idt = []
                    _put_token(char)
                    continue

                if char.isspace():
                    continue

                if char == self.comment:
                    # skip to the EOL
                    self._in_comment = True
                    continue

                idt.append(char)

        self._check_complete()

        return self._result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _error(self, msg=None, etype=None):
        """
        Parsing error. Raise exception
        """

        _emsg = ""
        _pre = _("Parse error on line %d" % self._lineno)
        
        if etype == self.error_unexpected and msg and len(msg) == 2:
            _emsg = _("Unexpected token '%s'. '%s' expected" % (msg[0], msg[1]))
        elif msg:
            _emsg = msg
        else:
            _emsg = _("Syntax error")

        raise ParseError("%s: %s" % (_pre, _emsg))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _process_state_init(self, word):
        if word == self.keyword:
            self._parsed_obj = ParsedBlockData()
            self._state = self.STATE_NAME_OR_OPEN
        else:
            self._error(msg=(word, self.keyword),
                       etype=self.error_unexpected)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _process_state_name_or_open(self, word):
        if word == "{":
            if self.has_name:
                 self._error(_("Block name required"))
            else:
                self._state = self.STATE_VARIABLE
                return

        # Else word is supposed to be a name of block
        if not self.has_name:
            self._error(_("Block name is not allowed: %s" % word))
        else:
            self._state = self.STATE_BLOCK_OPEN
            self._parsed_obj.set_name(word)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _process_state_block_open(self, word):
        if word != "{":
            self._error(msg=(word, "{"), etype=self.error_unexpected)
        else:
            self._state = self.STATE_VARIABLE

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _process_state_variable(self, word):
        if word == "}":
            # Closing block
            self._result.append(self._parsed_obj)
            self._cleanup()
            return
        if self.validvars:
            if word not in self.validvars:
                self._error(_("Unknown variable %s" % word))

        elif self.varre.match(word) is None:
            self._error(_("Invalid variable name: %s" % word))

        self._varname = word
        self._state = self.STATE_ASSIGN

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _process_state_assign(self, word):
        if word != self.assignchar:
            self._error(msg=(word, self.assignchar),
                       etype=self.error_unexpected)
        else:
            self._state = self.STATE_VALUE

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _process_state_value(self, word):
        self._parsed_obj.set(self._varname, word)
        self._varname = None
        self._state = self.STATE_VARIABLE

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _cleanup(self):
        """
        Set all neccessary variables to initial state
        """

        self._parsed_obj = None
        self._varname = None
        self._state = self.STATE_INIT
        self._in_comment = False
        self._in_quote = False

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _check_complete(self):
        """
        Check state after source reaches EOF for consistency
        """

        if self._in_quote:
            self._error(_("Unterminated quote"))

        if self._state != self.STATE_INIT:
            self._error(_("Unclosed block"))

#++++++++++++++++++++++++++++++++++++++++++++++++

class ParsedBlockData(object):
    """
    Parsed block data
    Provides dictionary-like access to parsed values
    """

    def __init__(self, name=None):
        self._name = name
        self._data = {}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def lookup(self, var):
        """
        Lookup for value of variable
        If variable does not exist, return None
        """

        if var in self._data:
            return self._data[var]
        else:
            return None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def set(self, var, val):
        """
        Set new value to variable
        """

        self._data[var] = val
