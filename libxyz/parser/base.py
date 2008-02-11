#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
#

from libxyz.exceptions import ParseError

class BaseParser(object):
    """
    Common parser interface

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
    * Escaping can only be used in rval position.
    """

    TOKEN_IDT = 0

    error_unexpected = 1

    def __init__(self, *args, **kwars):
        self._sdata = None
        self._escapechar = "\\"
        self._xqchar = "'"
        self._xqcount = 3
        self._xqtotal = 0
        self._skip_next = 0

        # Should be set to True when done parsing
        self._done = False
        # Should be set to True when parsing id can use escaped characters
        self._can_escape = False
        self._in_quote = False
        self._in_xquote = False
        self._in_comment = False
        # Keeps next token
        self._idt = []

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def parse(self, *args, **kwargs):
        raise NotImplementedError(_("Must be implemented in child class"))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def lexer(self, sdata, tokens, comment=None):
        """
        Scan input for lexemes and return to parser

        @param sdata: Source data
        @type sdata: L{libxyz.parser.SourceData}
        @param comment: Comment char
        @return: typle (token_type, token_value)
        """

        _escaped = False

        self._sdata = sdata

        for char in sdata:
            if self._done:
                raise StopIteration()

            if self._in_comment and char != "\n":
                continue

            if self._skip_next == 0:
                if 0 < self._xqtotal < self._xqcount:
                    if char != self._xqchar:
                        # Put read-ahead chars back
                        _back_tk = "%s%s" % (self._xqchar * self._xqtotal, char)
                        sdata.unget(_back_tk)
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
                if _escaped:
                    self._idt.append(char)
                    _escaped = False
                    continue

                if char == self._escapechar:
                    _escaped = True
                    continue

            if char == "\n":
                if self._in_quote:
                    self.error(_("Unterminated quote"))
                elif self._idt:
                    yield (self.TOKEN_IDT, "".join(self._idt))

                    self._idt = []
                    if char in tokens:
                        yield (self.TOKEN_IDT, char)

                self._in_comment = False
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

            if char in tokens or char.isspace():
                # Check if we finished assembling the word
                if self._idt:
                    yield (self.TOKEN_IDT, "".join(self._idt))
                    self._idt = []
                if not char.isspace():
                    yield (self.TOKEN_IDT, char)
                continue

            if char == comment and not self._in_xquote:
                # skip to the EOL
                self._in_comment = True
                continue

            self._idt.append(char)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def error(self, msg=None, etype=None):
        """
        Parsing error. Raise exception
        """

        _emsg = ""
        _pre = _("Parse error on line %d" % self._sdata.lineno)
        
        if etype == self.error_unexpected and msg and len(msg) == 2:
            _emsg = _("Unexpected token '%s'. Waiting for '%s'" % \
                    (msg[0].encode("string-escape"),
                     msg[1].encode("string-escape")))
        elif msg:
            _emsg = msg
        else:
            _emsg = _("Syntax error")

        raise ParseError("%s: %s" % (_pre, _emsg))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_idt(self):
        return self._idt
