#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008-2009
#
# This file is part of XYZCommander.
# XYZCommander is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# XYZCommander is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser Public License for more details.
# You should have received a copy of the GNU Lesser Public License
# along with XYZCommander. If not, see <http://www.gnu.org/licenses/>.

# Parsers tests

import re
import unittest
import locale
import gettext
import __builtin__
from nose.tools import raises

from libxyz.parser import BlockParser, MultiParser, FlatParser, RegexpParser
from libxyz.exceptions import ParseError, XYZValueError

__builtin__.__dict__["xyzenc"] = locale.getpreferredencoding()

def setup():
    gettext.install("xyzcmd")

class TestBlock(object):
    def setUp(self):
        self.p = BlockParser()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    @raises(XYZValueError)
    def testOptType(self):
        """
        Raise error on wrong opt type
        """

        BlockParser(1)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @raises(ParseError)
    def testQuote(self):
        """
        Parsing should raise ParseError on unterminated quotes
        """

        ParseError(self.p.parse("block {a = \"string\n}"))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testXQuote(self):
        """
        Test extended quotes
        """

        assert len(self.p.parse(
            "block { x = ''' ssaf \t \n ; \" ' '' ; & }''' }"))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testEmptyQuote(self):
        """
        Test parsing empty string value: ""
        """

        assert len(self.p.parse('block { x = "" }'))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testEmptyXQuote(self):
        """
        Test parsing empty x-quote
        """

        assert len(self.p.parse("block { x = '''''' }"))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testComments(self):
        """
        Test proper commenting
        """

        assert len(self.p.parse(
            "# \tComment 1\n#Comment 2 ''' = }{\n block {}")) == 0

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @raises(ParseError)
    def testInit(self):
        """
        In STATE_INIT state only keyword is acceptable
        """

        self.p.parse("anything")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @raises(ParseError)
    def testUnknownVar(self):
        """
        Variable not in valid list is not allowed
        """

        _opt = {"validvars": ("a",)}
        BlockParser(_opt).parse("block {b = 1}")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @raises(ParseError)
    def testValidVar(self):
        """
        Invalid variable name should raise exception
        """

        self.p.parse("block {a+-; = 1}")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testAssignChar1(self):
        """
        Test for assign character
        """

        _opt = {"assignchar": ":"}
        _p = BlockParser(_opt)
        assert len(_p.parse("block {a: 1}"))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testAssignChar2(self):
        """
        Test for assign character
        """

        _opt = {"assignchar": ":"}
        _p = BlockParser(_opt)
        assert len(_p.parse("block {a: 1}"))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @raises(ParseError)
    def testDelimiter1(self):
        """
        Correct delimiter should be supplied
        """

        _opt = {"delimiter": ";"}
        _p = BlockParser(_opt)
        _p.parse("block {a = 1\nb = 2\n}")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testDelimiter2(self):
        """
        Correct delimiter should be supplied
        """

        _opt = {"delimiter": ";"}
        _p = BlockParser(_opt)
        assert len(_p.parse("block {a = 1;b = 2} block2 {x=y;y=x}"))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @raises(ParseError)
    def testCompleteQuote(self):
        """
        Check for unclosed quote upon EOF
        """

        self.p.parse("block {a = \"string")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @raises(ParseError)
    def testCompleteBlock(self):
        """
        Check for unclosed block upon EOF
        """

        self.p.parse("block {a = value\n")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @raises(ParseError)
    def testValueValidator1(self):
        """
        Check if value_validator raises exception1
        """

        def _f(block, var, val):
            if val != "CORRECT_VALUE":
                raise XYZValueError("Incorrect value %s!" % val)

            return val

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        _opt = {"value_validator": _f}
        _p = BlockParser(_opt)
        _p.parse("block { a = INCORRECT_VALUE }")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @raises(ParseError)
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
        _p.parse("block { &m = INCORRECT_VALUE\n test = &m }")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @raises(ParseError)
    def testVarTransformation1(self):
        """
        Check for correct var transformation
        """

        def _f(a):
            raise XYZValueError(a)

        _opt = {"var_transform": _f}
        _p = BlockParser(_opt)

        _p.parse("block { a = VALUE }")

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

        assert len(_p.parse("block { a = CORRECT_VALUE }"))

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

        len(_p.parse("block { &m = CORRECT_VALUE\n a = &m }"))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testVarTransformation2(self):
        """
        Check for correct var transformation
        """

        _opt = {"var_transform": lambda x: x * 3}

        _p = BlockParser(_opt)
        _data = _p.parse("block { X = 1 }")

        assert "XXX" in _data["block"]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testEscaping(self):
        """
        Check for proper escaping
        """

        assert len(self.p.parse("block { var = a\\ b\\ c }"))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testListValue(self):
        """
        Check for proper list values parsing
        """

        _src = "block { var = l, i, s ,t }"

        _r = self.p.parse(_src)
        assert isinstance(_r["block"]["var"], tuple)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @raises(ParseError)
    def testUndefinedMacro(self):
        """
        Check for undefined macro
        """

        self.p.parse("block { a = &undef }")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestMulti(object):
    @raises(XYZValueError)
    def testArgs(self):
        """
        Check if raises on invalid arg type
        """

        MultiParser("WRONG")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @raises(ParseError)
    def testUnknownKeyword(self):
        """
        Test for unknown keyword
        """

        MultiParser({}).parse("keyword")

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
        assert data

#++++++++++++++++++++++++++++++++++++++++++++++++

class TestFlat(object):
    def setUp(self):
        self.p = FlatParser()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testComments(self):
        """
        Test for source type
        """

        _opt = {"comment": "*"}
        _p = FlatParser(_opt)

        assert len(_p.parse("* \tComment 1\n*Comment 2 ''' = }{\n A: B"))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @raises(ParseError)
    def testAssignChar(self):
        """
        Test for assign character
        """

        self.p.parse("X = Y")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @raises(ParseError)
    def testDelimChar1(self):
        """
        Test for delimiter character
        """

        self.p.parse("X = Y; Y = X")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testDelimChar2(self):
        """
        Test for delimiter character
        """

        _p = FlatParser({"delimiter": ";"})
        assert len(_p.parse("X: Y; Y: X"))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @raises(ParseError)
    def testComplete(self):
        """
        Check for complete expression
        """

        self.p.parse("X:")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @raises(ParseError)
    def testUnknownVar1(self):
        """
        Variable not in valid list is not allowed
        """

        _opt = {"validvars": ("A",)}
        FlatParser(_opt).parse("X: Y")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testUnknownVar2(self):
        """
        Variable in valid list is allowed
        """

        _opt = {"validvars": ("A",)}
        assert FlatParser(_opt).parse("A: Y")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @raises(ParseError)
    def testValueValidator1(self):
        """
        Check if value_validator raises exception 2
        """

        def _f(var, val):
            if val != "CORRECT_VALUE":
                raise XYZValueError("Incorrect value %s!" % val)

            return val

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        _opt = {"value_validator": _f}
        _p = FlatParser(_opt)

        _p.parse("A: INCORRECT_VALUE")

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

        assert self.p.parse("A: CORRECT_VALUE")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testListValue(self):
        """
        Check for proper list values parsing
        """

        _p = FlatParser()
        _src = "var : l, i, s ,t"

        _r = _p.parse(_src)
        assert isinstance(_r["var"], tuple)

#++++++++++++++++++++++++++++++++++++++++++++++++

class TestRegexp(unittest.TestCase):
    res = False

    @raises(ParseError)
    def testCBFailure(self):
        """
        Test for callback raising exceptions
        """

        def cb(mo):
            raise XYZValueError(u"Test error")

        _p = RegexpParser({re.compile("^test line$"): cb})
        _src = "test line"

        _p.parse(_src)

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

        assert self.res

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @raises(ParseError)
    def testUnmatched(self):
        """
        Test for umatched line
        """

        def cb(mo):
            return

        _p = RegexpParser({re.compile("^test line$"): cb})
        _src = "NOT a test line"

        _p.parse(_src)
