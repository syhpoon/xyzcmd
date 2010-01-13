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

# UI tests

from nose.tools import raises

from libxyz.ui import colors
from libxyz.exceptions import XYZValueError

import __builtin__
import locale

def setup():
    __builtin__._ = lambda x: x
    __builtin__.xyzenc = locale.getpreferredencoding()

class TestColors(object):
    @raises(XYZValueError)
    def testForegroundColor1(self):
        """
        Raise error on wrong color
        """

        colors.Foreground("AAA")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testForegroundColor2(self):
        """
        Check correct color
        """

        assert colors.Foreground("BLACK")
        assert colors.Foreground("DARK_BLUE")
        assert colors.Foreground("LIGHT_RED")
        assert colors.Foreground("DEFAULT")

        assert colors.Foreground("BLACK")
        assert colors.Foreground("BROWN")
        assert colors.Foreground("YELLOW")
        assert colors.Foreground("WHITE")
        assert colors.Foreground("DEFAULT")

        assert colors.Foreground("DARK_BLUE")
        assert colors.Foreground("DARK_MAGENTA")
        assert colors.Foreground("DARK_CYAN")
        assert colors.Foreground("DARK_RED")
        assert colors.Foreground("DARK_GREEN")
        assert colors.Foreground("DARK_GRAY")

        assert colors.Foreground("LIGHT_GRAY")
        assert colors.Foreground("LIGHT_RED")
        assert colors.Foreground("LIGHT_GREEN")
        assert colors.Foreground("LIGHT_BLUE")
        assert colors.Foreground("LIGHT_MAGENTA")
        assert colors.Foreground("LIGHT_CYAN")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @raises(XYZValueError)
    def testBackgroundColor1(self):
        """
        Raise error on wrong color
        """

        colors.Background("AAA")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testBackgroundColor2(self):
        """
        Check correct color
        """

        assert colors.Background("BLACK")
        assert colors.Background("BROWN")
        assert colors.Background("DEFAULT")

        assert colors.Background("DARK_RED")
        assert colors.Background("DARK_GREEN")
        assert colors.Background("DARK_BLUE")
        assert colors.Background("DARK_MAGENTA")
        assert colors.Background("DARK_CYAN")

        assert colors.Background("LIGHT_GRAY")


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @raises(XYZValueError)
    def testAttributeColor1(self):
        """
        Raise error on wrong attribute
        """

        colors.Attribute("AAA")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testAttributeColor2(self):
        """
        Check correct attribute
        """

        assert colors.Attribute("BOLD")
        assert colors.Attribute("UNDERLINE")
        assert colors.Attribute("BLINK")
        assert colors.Attribute("STANDOUT")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @raises(XYZValueError)
    def testHighForegroundColorIncorrect(self):
        colors.ForegroundHigh("WTF?")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @raises(XYZValueError)
    def testHighBackgroundColorIncorrect(self):
        colors.ForegroundHigh("WTF?")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _testHighColorCorrect(self, cl):
        assert colors.ForegroundHigh("#009")
        assert colors.ForegroundHigh("#fcc")
        assert colors.ForegroundHigh("g40")
        assert colors.ForegroundHigh("g#cc")
        assert colors.ForegroundHigh("h8")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testForegroundHighColorCorrect(self):
        self._testHighColorCorrect(colors.ForegroundHigh)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testBackgroundHighColorCorrect(self):
        self._testHighColorCorrect(colors.BackgroundHigh)
