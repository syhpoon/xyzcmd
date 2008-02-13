#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
#

from libxyz.parser import BaseParser, SourceData
from libxyz.exceptions import XYZValueError, ParseError

class FlatParser(BaseParser):
    """
    FlatParser is simple linear parser. It is used to parse
    variable = value statements.
    """

    STATE_INIT = 0
    STATE_VARIABLE = 1
    STATE_ASSIGN = 2
    STATE_VALUE = 3

    DEFAULT_OPT = {
                   "comment": "#",
                   "assignchar": ":",
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
        """

        super(FlatParser, self).__init__()

        self.opt = opt or self.DEFAULT_OPT

        for _opt in self.DEFAULT_OPT.keys():
            setattr(self, _opt, self.opt.get(_opt, self.DEFAULT_OPT[_opt]))

        self._result = {}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def parse(self, source):
        """
        Begin parsing
        """

        self._result = {}

        self._cleanup()

        _tokens = (self.assignchar,)

        if isinstance(source, SourceData):
            sdata = source
        else:
            sdata = SourceData(source)

        for _lex, _val in self.lexer(sdata, _tokens, self.comment)
            self._parse_table[self._state](_val)

        self._check_complete()

        return self._result
