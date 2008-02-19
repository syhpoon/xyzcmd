#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
#


import unittest

from libxyz.parser import BlockParser, MultiParser, FlatParser
from libxyz.exceptions import ParseError, XYZValueError

class BlockParsing(unittest.TestCase):
    def testOptType(self):
        """
        Raise error on wrong opt type
        """

        self.assertRaises(XYZValueError, BlockParser, 1)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testQuote(self):
        """
        Parsing should raise ParseError on unterminated quotes
        """

        self.assertRaises(ParseError, BlockParser().parse,
                          "block {a = \"string\n}")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testXQuote(self):
        """
        Test extending qutes
        """

        _p = BlockParser()
        self.assert_(len(_p.parse(
                     "block { x = ''' ssaf \t \n ; \" ' '' ; & }''' }")))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testComments(self):
        """
        Test proper commenting
        """

        _p = BlockParser()
        self.assert_(len(_p.parse(
                     "# \tComment 1\n#Comment 2 ''' = }{\n block {}")))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testInit(self):
        """
        In STATE_INIT state only keyword is acceptable
        """

        self.assertRaises(ParseError, BlockParser().parse, "anything")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testUnknownVar(self):
        """
        Variable not in valid list is not allowed
        """

        _opt = {"validvars": ("a",)}
        self.assertRaises(ParseError,
                          BlockParser(_opt).parse, "block {b = 1}")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testValidVar(self):
        """
        Invalid variable name should raise exception
        """

        self.assertRaises(ParseError,
                          BlockParser().parse, "block {a+-; = 1}")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testAssignChar1(self):
        """
        Test for assign character
        """

        _opt = {"assignchar": ":"}
        _p = BlockParser(_opt)
        self.assert_(len(_p.parse("block {a: 1}")))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testAssignChar2(self):
        """
        Test for assign character
        """

        _opt = {"assignchar": ":"}
        _p = BlockParser(_opt)
        self.assert_(len(_p.parse("block {a: 1}")))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testDelimiter1(self):
        """
        Correct delimiter should be supplied
        """

        _opt = {"delimiter": ";"}
        _p = BlockParser(_opt)
        self.assertRaises(ParseError, _p.parse, "block {a = 1\nb = 2\n}")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testDelimiter2(self):
        """
        Correct delimiter should be supplied
        """

        _opt = {"delimiter": ";"}
        _p = BlockParser(_opt)
        self.assert_(len(_p.parse("block {a = 1;b = 2} block2 {x=y;y=x}")))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testCompleteQuote(self):
        """
        Check for unclosed quote upon EOF
        """

        self.assertRaises(ParseError, BlockParser().parse,
                          "block {a = \"string")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testCompleteBlock(self):
        """
        Check for unclosed block upon EOF
        """

        self.assertRaises(ParseError, BlockParser().parse,
                          "block {a = value\n")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testValueValidator1(self):
        """
        Check fo value_validator raises exception
        """

        def _f(var, val):
            if val != "CORRECT_VALUE":
                raise ValueError("Incorrect value %s!" % val)

            return True

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        _opt = {"value_validator": _f}

        _p = BlockParser(_opt)

        self.assertRaises(ParseError, _p.parse, "block { a = INCORRECT_VALUE }")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testValueValidator2(self):
        """
        Check fo value_validator raises exception
        """

        def _f(var, val):
            if val != "CORRECT_VALUE":
                raise ValueError("Incorrect value %s!" % val)

            return True

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        _opt = {"value_validator": _f}

        _p = BlockParser(_opt)

        self.assert_(len(_p.parse("block { a = CORRECT_VALUE }")))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testEscaping(self):
        """
        Check for proper escaping
        """

        _p = BlockParser()
        _src = "block { var = a\\ b\\ c }"

        self.assert_(len(_p.parse(_src)))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testListValue(self):
        """
        Check for proper list values parsing
        """

        import types

        _p = BlockParser()
        _src = "block { var = l, i, s ,t }"

        _r = _p.parse(_src)
        self.assert_(type(_r["block"]["var"]) == types.TupleType)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MultiParsing(unittest.TestCase):
    def testArgs(self):
        """
        Check if raises on invalid arg type
        """

        self.assertRaises(XYZValueError, MultiParser, "WRONG")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testUnknownKeyword(self):
        """
        Test for unknown keyword
        """

        self.assertRaises(ParseError, MultiParser({}).parse, "keyword")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testParsing(self):
        """
        Try to parse some real config file
        """

        src = """\
AUTHOR: "Max E. Kuznecov <mek@mek.uz.ua>"
VERSION: "0.1"
DESCRIPTION: "Default XYZ skin"

fs.type {
	file = LIGHT_GRAY
	dir = WHITE
	block = DARK_MAGENTA
	char = LIGHT_MAGENTA
	link = LIGHT_CYAN
	fifo = DARK_CYAN
	socket = DARK_RED
}

fs.regexp {
	'''*.core$''' = DARK_RED
	'''\.+''' = LIGHT_GREY
}

"""
        import re

        _opt = {"count": 1}

        _type = BlockParser(_opt)
        _flat = FlatParser(_opt)
        _opt["varre"] = re.compile(".+")
        _regexp = BlockParser(_opt)

        _parsers = {"fs.type": _type,
                    "fs.regexp": _regexp,
                    ("AUTHOR", "VERSION", "DESCRIPTION"): _flat,
                    }

        _opt2 = {"tokens": (":",)}
        multi = MultiParser(_parsers, _opt2)

        data = multi.parse(src)
        self.assert_(data)

#++++++++++++++++++++++++++++++++++++++++++++++++

class FlatParsing(unittest.TestCase):
    def testComments(self):
        """
        Test for source type
        """

        _opt = {"comment": "*"}
        _p = FlatParser(_opt)

        self.assert_(len(_p.parse(
                     "* \tComment 1\n*Comment 2 ''' = }{\n A: B")))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testAssignChar(self):
        """
        Test for assign character
        """

        self.assertRaises(ParseError, FlatParser().parse, "X = Y")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testDelimChar1(self):
        """
        Test for delimiter character
        """

        self.assertRaises(ParseError, FlatParser().parse, "X = Y; Y = X")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testDelimChar(self):
        """
        Test for delimiter character
        """

        _p = FlatParser({"delimiter": ";"})
        self.assert_(len(_p.parse("X: Y; Y: X")))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testComplete(self):
        """
        Check for complete expression
        """

        self.assertRaises(ParseError, FlatParser().parse, "X:")

#++++++++++++++++++++++++++++++++++++++++++++++++

if __name__ == "__main__":
    import gettext
    gettext.install("xyzcmd")
    unittest.main()
