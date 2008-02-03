#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
#

from libxyz.exceptions import ParseError

class BaseParser(object):
    """
    Common parser interface
    """

    TOKEN_IDT = 0

    error_unexpected = 1

    def __init__(self, *args, **kwars):
        self._lineno = 1
        # Should be set to True when done parsing
        self._done = False
        # Should be set to True when parsing id can use escaped characters
        self._can_escape = False
        self._in_quote = False
        self._in_comment = False
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

        @param delimiter: Character that terminates statement

        @return: typle (token_type, token_value)
        """

        _escape = '\\'
        _escaped = False

        self._lineno = 1

        for char in sdata:
            if self._done:
                raise StopIteration()

            # Escape only when allowed, usually in values
            if self._can_escape:
                if _escaped:
                    self._idt.append(char)
                    _escaped = False
                    continue

                if char == _escape:
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
                self._lineno += 1
                continue

            if self._in_comment:
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

            if char == comment:
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
        _pre = _("Parse error on line %d" % self._lineno)
        
        if etype == self.error_unexpected and msg and len(msg) == 2:
            _emsg = _("Unexpected token '%s'. Waiting for '%s'" % \
                    (msg[0].encode("string-escape"),
                     msg[1].encode("string-escape")))
        elif msg:
            _emsg = msg
        else:
            _emsg = _("Syntax error")

        raise ParseError("%s: %s" % (_pre, _emsg))
