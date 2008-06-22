#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <syhpoon@syhpoon.name> 2008
#

import re
import unittest

from libxyz.parser import BlockParser, MultiParser, FlatParser, RegexpParser
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
        Check if value_validator raises exception
        """

        def _f(block, var, val):
            if val != "CORRECT_VALUE":
                raise XYZValueError("Incorrect value %s!" % val)

            return val

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        _opt = {"value_validator": _f}

        _p = BlockParser(_opt)

        self.assertRaises(ParseError, _p.parse, "block { a = INCORRECT_VALUE }")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testMacroValueValidator1(self):
        """
        Check if value_validator raises exception on macro
        """

        def _f(block, var, val):
            if val != "CORRECT_VALUE":
                raise XYZValueError("Incorrect value %s!" % val)

            return val

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        _opt = {"value_validator": _f}

        _p = BlockParser(_opt)

        self.assertRaises(ParseError, _p.parse, "block { &m = INCORRECT_VALUE\n test = &m }")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testValueValidator2(self):
        """
        Check for value_validator correct value
        """

        def _f(block, var, val):
            if val != "CORRECT_VALUE":
                raise XYZValueError("Incorrect value %s!" % val)

            # Returning modified value
            return 1

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        _opt = {"value_validator": _f}

        _p = BlockParser(_opt)

        self.assert_(len(_p.parse("block { a = CORRECT_VALUE }")))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testMacroValueValidator2(self):
        """
        Check for value_validator correct value on macro
        """

        def _f(block, var, val):
            if val != "CORRECT_VALUE":
                raise XYZValueError("Incorrect value %s!" % val)

            # Returning modified value
            return 1

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        _opt = {"value_validator": _f}

        _p = BlockParser(_opt)

        self.assert_(len(_p.parse("block { &m = CORRECT_VALUE\n a = &m }")))

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

        _p = BlockParser()
        _src = "block { var = l, i, s ,t }"

        _r = _p.parse(_src)
        self.assert_(isinstance(_r["block"]["var"], tuple))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testUndefinedMacro(self):
        """
        Check for undefined macro
        """

        _p = BlockParser()

        self.assertRaises(ParseError, _p.parse, "block { a = &undef }")

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
        Try to parse some dummy config file
        """

        src = """\
AUTHOR: "Max E. Kuznecov <syhpoon@syhpoon.name>"
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
	'''.+\.core$''' = DARK_RED
	'''\.+''' = LIGHT_GREY
}

ui.block1 {
    a = 1
    b = 2
}

ui.block2 {
    c = 1
    d = 2
}

"""
        import re

        _opt = {"count": 1}

        _type = BlockParser(_opt)
        _flat = FlatParser(_opt)
        _ui = BlockParser(_opt)
        _opt["varre"] = re.compile(".+")
        _regexp = BlockParser(_opt)

        _parsers = {"fs.type": _type,
                    "fs.regexp": _regexp,
                    ("AUTHOR", "VERSION", "DESCRIPTION"): _flat,
                    re.compile("^ui\.(\w+)$"): _ui,
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

    def testDelimChar2(self):
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

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testUnknownVar1(self):
        """
        Variable not in valid list is not allowed
        """

        _opt = {"validvars": ("A",)}
        self.assertRaises(ParseError, FlatParser(_opt).parse, "X: Y")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testUnknownVar2(self):
        """
        Variable in valid list is allowed
        """

        _opt = {"validvars": ("A",)}
        self.assert_(FlatParser(_opt).parse("A: Y"))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testValueValidator1(self):
        """
        Check if value_validator raises exception
        """

        def _f(var, val):
            if val != "CORRECT_VALUE":
                raise XYZValueError("Incorrect value %s!" % val)

            return val

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        _opt = {"value_validator": _f}

        _p = FlatParser(_opt)

        self.assertRaises(ParseError, _p.parse, "A: INCORRECT_VALUE")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testValueValidator2(self):
        """
        Check if value_validator accepts correct value
        """

        def _f(var, val):
            if val != "CORRECT_VALUE":
                raise XYZValueError("Incorrect value %s!" % val)

            return val

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        _opt = {"value_validator": _f}

        _p = FlatParser(_opt)

        self.assert_(_p.parse("A: CORRECT_VALUE"))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testListValue(self):
        """
        Check for proper list values parsing
        """

        _p = FlatParser()
        _src = "var : l, i, s ,t"

        _r = _p.parse(_src)
        self.assert_(isinstance(_r["var"], tuple))

#++++++++++++++++++++++++++++++++++++++++++++++++

class RegexpParsing(unittest.TestCase):
    res = False

    def testCBFailure(self):
        """
        Test for callback raising exceptions
        """

        def cb(mo):
            raise XYZValueError(u"Test error")

        _p = RegexpParser({re.compile("^test line$"): cb})
        _src = "test line"

        self.assertRaises(ParseError, _p.parse, _src)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testCBSuccess(self):
        """
        Test for callback success
        """

        self.res = False

        def cb(mo):
            self.res = True

        _p = RegexpParser({re.compile("^test line$"): cb})
        _src = "test line"

        _p.parse(_src)

        self.assert_(self.res)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testUnmatched(self):
        """
        Test for umatched line
        """

        def cb(mo):
            return

        _p = RegexpParser({re.compile("^test line$"): cb})
        _src = "NOT a test line"

        self.assertRaises(ParseError, _p.parse, _src)

#++++++++++++++++++++++++++++++++++++++++++++++++

if __name__ == "__main__":
    import gettext
    gettext.install("xyzcmd")
    unittest.main()
