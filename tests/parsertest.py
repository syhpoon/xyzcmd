#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
#


import unittest

from libxyz.parser import BlockParser, MultiParser
from libxyz.exceptions import ParseError, XYZValueError

class BlockParsing(unittest.TestCase):
    def testQuote(self):
        """
        Parsing should raise ParseError on unterminated quotes
        """

        self.assertRaises(ParseError, BlockParser("block").parse,
                          "block {a = \"string\n}")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testXQuote(self):
        """
        Test extending qutes
        """

        _p = BlockParser("block")
        self.assert_(len(_p.parse(
                     "block { x = ``` ssaf \t \n ; \" ' `` ; & }``` }")))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testComments(self):
        """
        Test proper commenting
        """

        _p = BlockParser("block")
        self.assert_(len(_p.parse(
                     "# \tComment 1\n#Comment 2 ``` = }{\n block {}")))

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

        _opt = {"has_name": True}
        self.assertRaises(ParseError,
                          BlockParser("block", _opt).parse,
                          "block {}")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testHasNoBlockName(self):
        """
        If has_name is False, block name is not allowed
        """

        _opt = {"has_name": False}
        self.assertRaises(ParseError,
                          BlockParser("block", _opt).parse, "block name {}")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testUnknownVar(self):
        """
        Variable not in valid list is not allowed
        """

        _opt = {"validvars": ("a",)}
        self.assertRaises(ParseError,
                          BlockParser("block", _opt).parse, "block {b = 1}")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testValidVar(self):
        """
        Invalid variable name should raise exception
        """

        self.assertRaises(ParseError,
                          BlockParser("block").parse, "block {a+-; = 1}")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testAssignChar(self):
        """
        Test for assign character
        """

        _opt = {"assignchar": ":"}
        self.assertRaises(ParseError,
                          BlockParser("block", _opt).parse, "block {a = 1}")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testDelimiter(self):
        """
        Correct delimiter should be supplied
        """

        _opt = {"delimiter": ";"}
        self.assertRaises(ParseError,
                          BlockParser("block", _opt).parse,
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

        _opt = {"value_validator": _f}

        self.assertRaises(ParseError, BlockParser("block", _opt).parse,
                          "block { a = INCORRECT_VALUE }")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testEscaping(self):
        """
        Check for proper escaping
        """

        _p = BlockParser("block")
        _src = "block { var = a\\ b\\ c }"

        self.assert_(len(_p.parse(_src)))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MultiParsing(unittest.TestCase):
    def testArgs(self):
        """
        Check if raises on invalid arg type
        """

        self.assertRaises(XYZValueError, MultiParser, "WRONG")

#++++++++++++++++++++++++++++++++++++++++++++++++

if __name__ == "__main__":
    import gettext
    gettext.install("xyzcmd")
    unittest.main()
