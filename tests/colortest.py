#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
#

import unittest

from libxyz.ui import colors
from libxyz.exceptions import XYZValueError

class ColorsTest(unittest.TestCase):
    def testForegroundColor1(self):
        """
        Raise error on wrong color
        """

        self.assertRaises(XYZValueError, colors.Foreground, "AAA")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testForegroundColor(self):
        """
        Check correct color
        """

        self.assert_(colors.Foreground("BLACK"))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testBackgroundColor1(self):
        """
        Raise error on wrong color
        """

        self.assertRaises(XYZValueError, colors.Background, "AAA")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testBackgroundColor2(self):
        """
        Check correct color
        """

        self.assert_(colors.Background("BROWN"))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testMonochromeColor1(self):
        """
        Raise error on wrong color
        """

        self.assertRaises(XYZValueError, colors.Monochrome, "AAA")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def testMonochromeColor2(self):
        """
        Check correct color
        """

        self.assert_(colors.Monochrome("BOLD"))

#++++++++++++++++++++++++++++++++++++++++++++++++

if __name__ == "__main__":
    import gettext
    gettext.install("xyzcmd")
    unittest.main()
