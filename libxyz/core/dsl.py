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

from libxyz.core.utils import ustring

import libxyz.exceptions as ex

def instantiated(func):
    """
    Ensure the class has been instantiated
    """

    def wrap(cls, *args, **kwargs):
        if cls._instance is None:
            raise ex.DSLError(_(u"Class must be instantiated first!"))
        else:
            return func(cls, *args, **kwargs)

    wrap.__doc__ = func.__doc__
    
    return wrap

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def error(msg):
    raise DSLError(_(u"DSL Error: %s") % msg)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class XYZ(object):
    """
    XYZ DSL implementation object
    """

    api = ["let",
           "unlet",
           "load",
           "bind",
           "exec_file",
           "kbd",
           "action",
           "macro",
           ]

    macros = {}
    
    _instance = None
    _env = {}
    
    def __new__(cls, xyz):
        if cls._instance is not None:
            return cls._instance

        # Else init singleton
        cls.xyz = xyz
        cls._instance = cls

        cls._env = {"XYZ": cls}
        cls._env.update(dict([(f, getattr(cls, f)) for f in cls.api]))

        # Init macros
        cls.macros["ACT_PATH"] = lambda: cls.xyz.pm.from_load(
            ":sys:panel", "get_selected")().path

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

        _conf = cls.xyz.conf

        if sect not in _conf:
            _conf[sect] = {}
            
        if var in _conf[sect] and isinstance(_conf[sect][var], dict) and \
        isinstance(val, dict):
            # Update rather than overwrite
            _conf[sect][var].update(val)
        else:
            cls.xyz.conf[sect][var] = val

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def unlet(cls, var, sect=u"local"):
        """
        Unset variable
        """

        if var in cls.xyz.conf[sect]:
            del(cls.xyz.conf[sect])

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def load(cls, plugin):
        """
        Load method[s] from plugin
        """

        try:
            cls.xyz.km.load(plugin)
        except Exception as e:
            error(_(u"Unable to load plugin %s: %s") %
                  (plugin, ustring(str(e))))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def bind(cls, method, shortcut, context="@"):
        try:
            cls.xyz.km.bind(method, shortcut, context=context)
        except Exception as e:
            error(_(u"Unable to bind shortcut: %s") % (ustring(str(e))))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def kbd(cls, *args):
        return " ".join(args)
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def exec_file(cls, filename):
        """
        Execute DSL in file
        """

        with open(filename) as f:
            cls.execute(f.read())

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def action(cls, rule, fn):
        """
        Set up an action to be taken upon pressing action key on file
        """

        try:
            cls.xyz.am.register(rule, fn)
        except Exception as e:
            error(_(u"Unable to register action: %s") % ustring(str(e)))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def macro(cls, macroname):
        """
        Expand macro name.
        
        Availbale macros:
        * ACT_CWD        -- Working directory in active panel
        * INACT_CWD      -- Working directory in inactive panel
        * ACT_PATH       -- Full path to selected object in active panel
        * INACT_PATH     -- Full path to selected object in inactive panel
        * ACT_BASE       -- Parent directory in active panel
        * INACT_BASE     -- Parent directory in inactive panel
        * ACT_TAGGED     -- List of tagged files in active panel
        * INACT_TAGGED   -- List of tagged files in inactive panel
        * ACT_UNTAGGED   -- List of not tagged files in active panel
        * INACT_UNTAGGED -- List of not tagged files in inactive panel
        """

        if macroname in cls.macros:
            try:
                return cls.macros[macroname]()
            except Exception as e:
                xyzlog.warning(_(u"Unable to expand macro %s: %s") %
                               (ustring(macroname), ustring(str(e))))
        # Return unchanged
        return macroname
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    @classmethod
    @instantiated
    def execute(cls, source):
        """
        Execute DSL statements
        @param source: Either string or open file-object
        """

        try:
            exec source in cls._env
        except Exception as e:
            raise ex.DSLError(_(u"Error in DSL execution: %s") %
                                 ustring(str(e)))

#++++++++++++++++++++++++++++++++++++++++++++++++

## Auto-generate corresponding module-level functions
module = sys.modules[__name__]

__all__ = ["XYZ"]

for f in XYZ.api:
    setattr(module, f, getattr(XYZ, f))
    __all__.append(f)
