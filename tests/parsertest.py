#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
#


import unittest

from libxyz.parser import BlockParser
from libxyz.exceptions import ParseError

class BlockParsing(unittest.TestCase):
    def testQuote(self):
        """
        Parsing should raise ParseError on unterminated quotes
        """

        self.assertRaises(ParseError, BlockParser("block").parse,
                          "block {a = \"string\n}")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testInit(self):
        """
        In STATE_INIT state only keyword is acceptable
        """

        self.assertRaises(ParseError, BlockParser("block").parse, "anything")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testHasBlockName(self):
        """
        If has_name is True, block name must be defined
        """

        self.assertRaises(ParseError,
                          BlockParser("block", has_name=True).parse,
                          "block {}")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testHasNoBlockName(self):
        """
        If has_name is False, block name is not allowed
        """

        self.assertRaises(ParseError,
                          BlockParser("block", has_name=False).parse,
                          "block name {}")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testUnknownVar(self):
        """
        Variable not in valid list is not allowed
        """

        self.assertRaises(ParseError,
                          BlockParser("block", validvars=("a",)).parse,
                          "block {b = 1}")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testValidVar(self):
        """
        Invalid variable name should raise exception
        """

        self.assertRaises(ParseError,
                          BlockParser("block").parse,
                          "block {a+-; = 1}")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testAssignChar(self):
        """
        Test for assign character
        """

        self.assertRaises(ParseError,
                          BlockParser("block", assignchar=":").parse,
                          "block {a = 1}")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testDelimiter(self):
        """
        Correct delimiter should be supplied
        """

        self.assertRaises(ParseError,
                          BlockParser("block", delimiter=";").parse,
                          "block {a = 1\nb = 2\n}")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testCompleteQuote(self):
        """
        Check for unclosed quote upon EOF
        """

        self.assertRaises(ParseError, BlockParser("block").parse,
                          "block {a = \"string")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testCompleteBlock(self):
        """
        Check for unclosed block upon EOF
        """

        self.assertRaises(ParseError, BlockParser("block").parse,
                          "block {a = value\n")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testValueValidator(self):
        """
        Check fo value_validator raises exception
        """

        def _f(var, val):
            if val != "CORRECT_VALUE":
                raise ValueError("Incorrect value %s!" % val)

            return True

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.assertRaises(ParseError, BlockParser("block",
                          value_validator=_f).parse,
                          "block { a = INCORRECT_VALUE }")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testEscaping(self):
        """
        Check for proper escaping
        """

        _p = BlockParser("block")
        _src = "block { var = a\\ \\b\\ c }"

        self.assert_(len(_p.parse(_src)))

if __name__ == "__main__":
    import gettext
    gettext.install("xyzcmd")
    unittest.main()
