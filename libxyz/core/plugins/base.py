#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <syhpoon@syhpoon.name> 2008
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
from libxyz.ui.colors import Palette

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

    # Events provided by plugin
    # List of (event_name, event_desc) tuples
    EVENTS = None

    # Custom plugin palettes
    PALETTES = None

    def __init__(self, xyz, *args, **kwargs):
        self.xyz = xyz

        # Integer module version (for possible comparison)
        self.intversion = 0

        # Public methods dictionary
        # Accessed as plugin attribute (plugin.method())
        self.public = {}

        # Public data dictionary
        # Accessed as plugin items (plugin["data"])
        self.public_data = {}

        self.ns = Namespace(u":".join(("", self.NAMESPACE, self.NAME)))

        # Register custom palettes
        self._register_palettes(self.PALETTES)

        # Register plugin's constructor to be run upon startup
        self.xyz.hm.register("event:startup", self.prepare)

        try:
            self.conf = self.xyz.conf[u"plugins"][self.ns.pfull]
        except KeyError:
            self.conf = {}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __getattr__(self, method):
        """
        Provide transparent access to public methods
        """

        try:
            return self.public[method]
        except KeyError:
            raise AttributeError(_(u"%s is not a public method") % method)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __getitem__(self, obj):
        """
        Provide transparent access to public data
        """

        try:
            return self.public_data[obj]
        except KeyError:
            raise AttributeError(_(u"%s is not a public data object") % obj)

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

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def export(self, func):
        """
        Export method
        """

        _name = func.im_func.__name__

        func.im_func.ns = u"%s:%s" % (self.ns.full, _name)

        self.public[_name] = func

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def export_data(self, name, data):
        """
        Export data
        """

        self.public_data[name] = data

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def fire_event(self, event, *args):
        """
        Fire event
        """

        self.xyz.hm.dispatch(self.event_name(event), *args)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def event_name(self, short):
        """
        Return full event name
        """

        return "event%s:%s" % (self.ns.pfull, short)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _register_palettes(self, palettes):
        """
        Register custom plugin palettes in current skin
        """

        if palettes is None:
            return

        current_skin = self.xyz.skin.name

        for pname, p in palettes.iteritems():
            # Try current skin
            config = p.get(current_skin, None)

            # No entry for current skin, try default (None)
            if config is None:
                config = p.get(None, None)

                # No default entry - warn and continue
                if config is None:
                    xyzlog.error(_(u"Unable to register palette %s: "\
                                   u"neither entry for current skin (%s) "
                                   u"nor default one found") %
                                 (pname, current_skin))
                    continue

            palette = Palette(None, *Palette.convert(config))

            self.xyz.skin.add_custom_palette(u"ui."+self.ns.pfull,
                                             pname, palette)

            # Register new palette
            self.xyz.screen.register_palette(
                [palette.get_palette(self.xyz.driver)])
