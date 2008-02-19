#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
#

from libxyz.parser import SourceData
from libxyz.exceptions import LexerError

class Lexer(object):
    """
    Lexical analyzer

    Lexer rules:
    -----------
    * Blank chars are usually ignored. Except from in quoting.
    * Quote can be one-line: "quoted value", or multiline:
      '''quoted value1,
         quoted value2,
      '''
    * New-line char ends commented line if any.
    * Variable names are validated according to varre regexp.
    * Values can be provided as simple literals or quoted ones.
    * If value contains spaces or any other non-alphanumeric values it is better
      to quote it or escape it using escapechar.
    * Variable can take list of values, separated by comma
    * Escaping can only be used in rval position.
    """

    TOKEN_IDT = 0

    def __init__(self, source, tokens, comment="#"):
        """
        @param source: Parsing source. If file object is passed, it must be
                       closed by caller function after parsing completes.
        @type source: string, file-like object or SourceData object

        @param tokens: List of tokens
        @type tokens: sequence

        @param comment: Comment char
        """

        if isinstance(source, SourceData):
            self.sdata = source
        else:
            self.sdata = SourceData(source)

        self.tokens = tokens
        self.comment = comment

        self._escapechar = "\\"
        self._xqchar = "'"
        self._xqcount = 3
        self._xqtotal = 0
        self._skip_next = 0

        # Should be set to True when done parsing
        self._done = False
        # Should be set to True when parsing id can use escaped characters
        self._can_escape = False
        self._escaped = False
        self._in_quote = False
        self._in_xquote = False
        self._in_comment = False
        # Keeps next token
        self._idt = []

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def lexer(self):
        """
        Scan input for lexemes and return to parser

        @return: typle (token_type, token_value)
        """

        for char in self.sdata:
            if self._done:
                self.unget(char)
                return None

            if self._in_comment and char != "\n":
                continue

            if self._skip_next == 0:
                if 0 < self._xqtotal < self._xqcount:
                    if char != self._xqchar:
                        # Put read-ahead chars back
                        _back_tk = "%s%s" % (self._xqchar * self._xqtotal, char)
                        self.unget(_back_tk)
                        self._skip_next = len(_back_tk)
                        self._xqtotal = 0
                        continue

                if char == self._xqchar:
                    self._xqtotal += 1

                    # Assembled xquote
                    if self._xqtotal == self._xqcount:
                        if self._in_xquote:
                            # Finishing
                            self._in_xquote = False
                        else:
                            # Beginning
                            self._in_xquote = True

                        self._xqtotal = 0

                    continue
            else:
                self._skip_next -= 1

            if self._in_xquote:
                self._idt.append(char)
                continue

            # Escape only when allowed, usually in values
            if self._can_escape:
                if self._escaped:
                    self._idt.append(char)
                    self._escaped = False
                    continue

                if char == self._escapechar:
                    self._escaped = True
                    continue

            if char == "\n":
                if self._in_quote:
                    raise LexerError(_("Unterminated quote"))

                _token = None

                if self._idt:
                    _token = "".join(self._idt)
                    self._idt = []
                else:
                    self._in_comment = False

                if char in self.tokens:
                    if _token:
                        self.unget(char)
                    else:
                        _token = char

                if _token:
                    return (self.TOKEN_IDT, _token)
                else:
                    continue

            if char == '"':
                if self._in_quote:
                    self._in_quote = False
                else:
                    self._in_quote = True

                continue

            if self._in_quote:
                self._idt.append(char)
                continue

            if char in self.tokens or char.isspace():
                _token = None

                # Check if we finished assembling the token
                if self._idt:
                    _token = "".join(self._idt)
                    self._idt = []
                if not char.isspace():
                    if _token:
                        self.unget(char)
                    else:
                        _token = char

                if _token:
                    return (self.TOKEN_IDT, _token)
                else:
                    continue

            if char == self.comment and not self._in_xquote:
                # skip to the EOL
                self._in_comment = True
                continue

            self._idt.append(char)

        if self._idt:
            _token = "".join(self._idt)
            self._idt = []
            return (self.TOKEN_IDT, _token)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_idt(self):
        """
        Return current state of token buffer
        """

        return self._idt

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def done(self):
        """
        Order lexer to stop processing
        """

        self._done = True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def unget(self, token):
        """
        Put read token back to input stream
        """

        self.sdata.unget(token)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def escaping_on(self):
        """
        Enable escaping
        """

        self._can_escape = True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def escaping_off(self):
        """
        Disable escaping
        """

        self._can_escape = False
