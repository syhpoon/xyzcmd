#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
#

import types

from libxyz.parser import BaseParser, SourceData
from libxyz.exceptions import XYZValueError, ParseError

class MultiParser(BaseParser):
    """
    MultiParser is a simple container for any other parsers
    Usually parsers, such as BlockParser designed to parse homogeneous blocks in
    single source: file or string. But still it might be useful sometimes to
    parse multiple blocks of different syntax in single source.
    Thus, one can register few necessary parsers into MultiParser and go on.
    """

    DEFAULT_OPT = {
                   "comment": "#",
                   "tokens": (),
                   }

    def __init__(self, parsers, opt=None):
        """
        @param parsers: dictionary containing keyword as key and *Parser object
                        as value.
        @type parsers: dictionary

        @param opt: Options

        Available options:
            - comment: Comment character.
              Everything else ignored until EOL.
              Type: I{string (single char)}

            - tokens: List of tokens.
              Type: I{sequence}
        """

        super(MultiParser, self).__init__()

        if parsers:
            if type(parsers) != types.DictType:
                raise XYZValueError(_("Invalid argument type %s. "\
                                      "Dictionary expected" % str(parsers)))
            else:
                self.parsers = parsers
        else:
            self.parsers = {}

        self.opt = opt or self.DEFAULT_OPT
        self.set_opt(self.DEFAULT_OPT, self.opt)

        self._result = {}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def parse(self, source):
        """
        Begin parsing
        """

        self._result = {}

        if isinstance(source, SourceData):
            sdata = source
        else:
            sdata = SourceData(source)

        for _lex, _val in self.lexer(sdata, self.tokens, self.comment):
            if _lex == self.TOKEN_IDT:
                if _val in self.parsers:
                    # Push read token back
                    # Space at the end needed because it was consumed by
                    # lexer
                    sdata.unget(_val + " ")
                    self._result[_val] = self.parsers[_val].parse(sdata)
                else:
                    self.error(_("Unknown keyword: %s" % _val))

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
            raise XYZValueError(_("Invalid argument type %s. "\
                                  "BaseParser or subclassed expected" % \
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
