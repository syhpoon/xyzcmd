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

from libxyz.exceptions import PluginError
from libxyz.core.plugins import Namespace

class BasePlugin(object):
    """
    Parent class for all xyz-plugins
    """

    # NAME: Plugin name
    NAME = None

    # AUTHOR: Author name
    AUTHOR = None

    # VERSION: Plugin version
    VERSION = None

    # Brief one line description
    BRIEF_DESCRIPTION = None

    # Full plugin description
    FULL_DESCRIPTION = None

    # NAMESPACE: Plugin namespace. For detailed information about
    #            namespaces see Plugins chapter of XYZCommander user manual.
    NAMESPACE = None

    # MIN_XYZ_VERSION: Minimal XYZCommander version
    #                  the plugin is compatible with
    MIN_XYZ_VERSION = None

    # Plugin documentation
    DOC = None

    # Plugin home-page
    HOMEPAGE = None

    def __init__(self, xyz, *args, **kwargs):
        self.xyz = xyz

        # Integer module version (for possible comparison)
        self.intversion = 0

        # List of exported public methods
        self.public = {}

        self.ns = Namespace(u":".join(("", self.NAMESPACE, self.NAME)))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __getattr__(self, method):
        """
        Provide transparent access to public methods
        """

        if method in self.public:
            return self.public[method]
        else:
            raise AttributeError(_(u"%s is not a public method" % method))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def prepare(self, *args, **kwargs):
        """
        Plugin constructor
        """

        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def finalize(self, *args, **kwargs):
        """
        Plugin destructor
        """

        pass
