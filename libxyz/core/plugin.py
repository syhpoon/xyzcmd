#-*- coding: utf8 -*
#
# Max E. Kuznecov ~syhpoon <mek@mek.uz.ua> 2008
#

"""
Plugin is the main way to extend xyzcmd functionality.
Every single plugin should inherit BasePlugin interface.
Plugin exports its public methods via 'public' dictionary of BasePlugin class.
First plugin must be registered within one of xyz plugin namespaces.
Available namespaces are:
- ui    - User-interface related
- vfs   - Virtual file-system related
- misc  - Other miscellaneous

After methods are exported, they will be available under
xyz:plugins:<namespace>:<plugin-name> namespace
"""

from libxyz.exceptions import PluginError

class BasePlugin(object):
    """
    Parent class for all xyz-plugins
    """

    def __init__(self, name, meta, *args, **kwargs):
        """
        @param name: Plugin name
        @type name: string
        """

        self.name = name
        self.version = version[0]
        self.intversion = version[1]
        self.author = author
        self.bdescription = bdescription
        self.description = description

        # List of exported public methods
        self.public = {}

        self._name_internal = self.__class__.__name__

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def add_method(self, method):
        """
        Add method to public
        """

        if not callable(method):
            raise PluginError(_("Callable method required"))

        self.public[self._build_key(method)] = method

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def remove_method(self, name):
        """
        Remove method from public
        """

        try:
            del self.public[self._build_key(method)]
        except KeyError:
            pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _build_key(self, method):
        """
        Build full ierarchical method path
        """

        return ".".join(("xyz", self._name_internal, method.__name__))
