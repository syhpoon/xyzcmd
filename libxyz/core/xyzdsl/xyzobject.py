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

import sys

import libxyz.exceptions as ex


def instantiated(func):
    """
    Ensure the class has been instantiated
    """

    def wrap(cls, *args, **kwargs):
        if cls._instance is None:
            raise ex.XYZDSLError(_(u"Class must be instantiated first!"))
        else:
            return func(cls, *args, **kwargs)

    wrap.__doc__ = func.__doc__
    
    return wrap

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class XYZObject(object):
    """
    XYZ DSL implementation object
    """

    # Public API functions
    api = ["let", "load"]

    _instance = None
    
    def __new__(cls, xyz):
        if cls._instance is not None:
            return cls._instance

        # Else init singleton
        cls.xyz = xyz
        cls._instance = cls

        return cls

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def let(cls, var, val, sect=u"local"):
        """
        Set variable.
        Variable will be available in xyz.conf[section][varname]
        If section is not provided - local will be used
        """
        
        if sect not in cls.xyz.conf:
            cls.xyz.conf[sect] = {}

        cls.xyz.conf[sect][var] = val

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def load(cls, plugin):
        """
        Load method[s] from plugin
        """

        try:
            cls.xyz.pm.load(plugin)
        except Exception as e:
            raise ex.XYZDSLError(_(u"Unable to load plugin {plugin}: {e!s}")
                                 .format(*locals()))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def bind(cls, method, shortcut, context="@"):
        # TODO: if not isinstance(shortcut, XYZShortcut): ...
        self.xyz.km.bind(method, shortcut, context=context)

#++++++++++++++++++++++++++++++++++++++++++++++++

## Auto-generate all module-level counterpart functions
module = sys.modules[__name__]

for f in XYZObject.api:
    setattr(module, f, getattr(XYZObject, f))

__all__ = ["XYZObject"] + [f for f in XYZObject.api]
