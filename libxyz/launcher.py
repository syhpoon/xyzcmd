#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
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

"""
Launcher - all neccessary initialization
"""

import sys
import gettext
import getopt
import re
import os.path

import libxyz.ui as uilib
import libxyz.const as const

from libxyz.version import Version
from libxyz.core import Skin
from libxyz.core import XYZData
from libxyz.core.plugins import PluginManager
from libxyz.parser import BlockParser
from libxyz.parser import MultiParser
from libxyz.exceptions import XYZValueError

class Launcher(object):
    """
    Startup class
    """

    def __init__(self):
        """
        Initialization
        """

        gettext.install(u"xyzcmd")

        self.cmdopts = "c:vh"
        self.xyz = XYZData(
                            {
                            u"screen": None,
                            u"skin": None,
                            u"pm": None,
                            }
                          )

        self._conf_dir = None

        self._init_default()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _init_default(self):
        """
        Define some default values
        """

        self._conf_dir = const.CONF_DIR

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def run(self):
        """
        Run commander
        """

        self.parse_args()
        self.parse_configs()

        # TODO: real skin path from configs
        self.xyz.skin = Skin(u"/tmp/skins/default")
        # TODO: real plugins path from config
        self.xyz.pm = PluginManager(self.xyz, ['/tmp/plugins',])

        self.xyz.screen = uilib.display.init_display()
        self.xyz.screen.register_palette(self.xyz.skin.get_palette_list())
        self.xyz.screen.run_wrapper(self._run)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _run(self):
        _dim = self.xyz.screen.get_cols_rows()
        self._top = uilib.lowui.Filler(uilib.lowui.Text(""))

        _str = u"Welcome!\nAAAA\nBBBB\nCCCC"
        _title = u"XYZCommander"

        #_msg = uilib.YesNoBox(self.xyz, self._top, _str, _title)
        #self.xyz.screen.draw_screen(_dim, _msg.render(_dim, True))

        #say_hello = self.xyz.pm.from_load(u":misc:hello", u"SayHello")
        hello = self.xyz.pm.load(u":misc:hello")
        hello.say_hello(self._top)

        while not self.xyz.screen.get_input():
            pass

        self.finalize()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def parse_args(self):
        """
        Parse command line arguments
        """

        try:
            _opts, _args = getopt.getopt(sys.argv[1:], self.cmdopts)
        except getopt.GetoptError, e:
            print str(e)
            self.usage()
            self.quit()

        for _o, _a in _opts:
            if _c == "-c":
                self._conf_dir = _a
            elif _o == "-v":
                self.version()
                self.quit()
            else:
                self.usage()
                self.quit()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def parse_configs(self):
        """
        Parse configuration
        """

        self._parse_conf_xyz()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _parse_conf_xyz(self):
        """
        Parse main config
        """

        def _validate(block, var, val):
            if val == u"ENABLE":
                return True
            elif val == u"DISABLE":
                return False
            else:
                raise XYZValueError(_(u"Invalid value %s. "\
                                      u"Available are: ENABLED or DISABLE"))

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        _plugins_opts = {
                         "varre": re.compile("^[\w:-]+$"),
                         "assignchar": ">",
                         "value_validator": _validate,
                        }

        _block_plugins_p = BlockParser(_plugins_opts)

        _parser = MultiParser({})
        _parser.register("plugins", _block_plugins_p)

        _path = os.path.join(self._conf_dir, const.XYZ_CONF_FILE)
        _file = open(_path, "r")
        _data = _parser.parse(_file)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def usage(self):
        """
        Show usage
        """

        print _(u"""\
%s version %s
Usage: %s [-c dir][-vh]
    -c  -- Directory with configuration files
    -v  -- Show version
    -h  -- Show this help message\
""" % (const.PROG, Version.version, os.path.basename(sys.argv[0])))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def version(self):
        """
        Show version
        """

        print _(u"%s version %s" % (const.PROG, Version.version))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def quit(self):
        """
        Quit program
        """

        sys.exit()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def finalize(self):
        """
        Perform shutdown procedures
        """

        self.xyz.pm.shutdown()
