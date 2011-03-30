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
import os
import traceback
import __builtin__

from libxyz.core.utils import ustring
from libxyz.core.utils import is_func
from libxyz.core.plugins import Namespace
from libxyz.core import FSRule

from libxyz.ui.colors import Palette
from libxyz.ui import Shortcut

from skin import Skin

import libxyz.exceptions as ex

def instantiated(func):
    """
    Ensure the class has been instantiated
    """

    def wrap(cls, *args, **kwargs):
        if cls._instance is None:
            error(_(u"Class must be instantiated first!"))
        else:
            return func(cls, *args, **kwargs)

    wrap.__doc__ = func.__doc__

    return wrap

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def error(msg, trace=True):
    if trace and hasattr(__builtin__, "xyzlog"):
        xyzlog.debug(ustring(traceback.format_exc()))
    raise ex.DSLError(_(u"DSL Error: %s") % msg)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class XYZ(object):
    """
    XYZ DSL implementation object
    """

    api = ["let",
           "val",
           "section",
           "unlet",
           "load",
           "unload",
           "bind",
           "exec_file",
           "kbd",
           "action",
           "macro",
           "call",
           "env",
           "shell",
           "alias",
           "plugins_on",
           "plugins_off",
           "plugin_conf",
           "icmd",
           "prefix",
           "help",
           "vfs",
           "vfs_path",
           "hook",
           "unhook",
           "fsrule",
           "palette",
           "skin"
           ]

    EVENT_CONF_UPDATE = u"event:conf_update"

    macros = {}

    _instance = None
    _env = {}

    def __new__(cls, xyz):
        if cls._instance is not None:
            return cls._instance

        # Else init singleton
        cls.xyz = xyz
        cls._instance = super(XYZ, cls).__new__(cls)

        cls._env = {"XYZ": cls}
        cls._env.update(dict([(ff, getattr(cls, ff)) for ff in cls.api]))

        # Init macros
        cls.macros = {}
        cls.init_macros()

        return cls._instance

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    def init_macros(cls):
        cls.macros["ACT_CWD"] = lambda: cls.xyz.pm.from_load(":sys:panel",
                                                             "cwd")()
        cls.macros["INACT_CWD"] = lambda: cls.xyz.pm.from_load(":sys:panel",
                                                               "cwd")(False)

        cls.macros["ACT_PATH"] = lambda: \
                                   cls.xyz.pm.from_load(":sys:panel",
                                                        "get_selected")().path

        cls.macros["INACT_PATH"] = lambda: \
                                   cls.xyz.pm.from_load(":sys:panel",
                                                        "get_selected"
                                                        )(False).path
        cls.macros["ACT_BASE"] = lambda: \
                                 os.path.dirname(cls.macros["ACT_CWD"]())

        cls.macros["INACT_BASE"] = lambda: \
                                   os.path.dirname(cls.macros["INACT_CWD"]())

        cls.macros["ACT_TAGGED"] = lambda: [x.full_path for x in
                                            cls.xyz.pm.from_load(
                                                ":sys:panel",
                                                "get_tagged")()]
        cls.macros["INACT_TAGGED"] = lambda: [x.full_path for x in
                                              cls.xyz.pm.from_load(
                                                  ":sys:panel",
                                                  "get_tagged")(False)]

        cls.macros["ACT_UNTAGGED"] = lambda: [x.full_path for x in
                                              cls.xyz.pm.from_load(
                                                  ":sys:panel",
                                                  "get_untagged")()]
        cls.macros["INACT_UNTAGGED"] = lambda: [x.full_path for x in
                                                cls.xyz.pm.from_load(
                                                    ":sys:panel",
                                                    "get_untagged")(False)]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    def _clear(cls):
        cls._instance = None

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

        cls.xyz.hm.dispatch(cls.EVENT_CONF_UPDATE, var, val, sect)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def val(cls, var, sect=u"local"):
        """
        Return variable value or None if undefined
        """

        try:
            return cls.xyz.conf[sect][var]
        except Exception:
            return None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def section(cls, sect=u"local"):
        """
        Return whole configuration section contents as a dictionary or None
        if undefined
        """

        try:
            return cls.xyz.conf[sect]
        except Exception:
            return None

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
        except Exception, e:
            error(_(u"Unable to load plugin %s: %s") %
                  (plugin, unicode(e)))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def unload(cls, plugin):
        """
        Unload method[s] from plugin
        """

        try:
            if cls.xyz.pm.is_loaded(plugin):
                cls.xyz.pm.del_loaded(plugin)
        except Exception, e:
            error(_(u"Unable to unload plugin %s: %s") %
                  (plugin, unicode(e)))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def bind(cls, method, shortcut, context="DEFAULT"):
        """
        Bind method to shortcut
        """

        try:
            cls.xyz.km.bind(method, shortcut, context=context)
        except Exception, e:
            error(_(u"Unable to bind shortcut %s: %s") % (str(shortcut),
                                                          unicode(e)))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def kbd(cls, *args):
        """
        Create keyboard shortcut
        """

        return Shortcut(sc=list(args))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def exec_file(cls, filename):
        """
        Execute DSL in file
        """

        f = None

        try:
            f = open(filename)
            cls.execute(f.read())
        except Exception, e:
            error(_(u"Unable to execute file: %s") % unicode(e))

        if f:
            f.close()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def action(cls, rule, fn):
        """
        Set up an action to be taken upon pressing action key on file
        """

        try:
            cls.xyz.am.register(rule, fn)
        except Exception, e:
            error(_(u"Unable to register action: %s") % unicode(e))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def macro(cls, macroname):
        """
        Expand macro name.

        Available macros:
        * ACT_CWD        -- Working directory in active panel
        * INACT_CWD      -- Working directory in inactive panel
        * ACT_PATH       -- Full selected object path in active panel
        * INACT_PATH     -- Full selected object path in inactive panel
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
            except Exception, e:
                xyzlog.warning(_(u"Unable to expand macro %s: %s") %
                               (ustring(macroname), unicode(e)))
        # Return unchanged
        return macroname

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def call(cls, method, *args, **kwargs):
        """
        Call plugin method
        """

        try:
            p = Namespace(method)
            m = cls.xyz.pm.from_load(p.pfull, p.method)
            return m(*args, **kwargs)
        except Exception, e:
            error(_(u"Unable to execute method %s: %s") %
                  (method, unicode(e)))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def env(cls, var, default=None):
        """
        Return environment variable or default if is not set
        """

        return os.getenv(var, default)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def shell(cls, cmd, *args, **kwargs):
        """
        Execute command via :core:shell plugin
        Optional boolean argument 'current' can be provided to indicate
        that cmd is to be run from current directory.
        Optional boolean argument 'bg' can be provided to indicate that cmd
        must be executed in background
        Optional boolean argument 'reload' can be provided to indicate
        that panel content should/should not be reloaded after execution
        Optional boolean argument 'wait' can be provided to indicate
        that shell should/should not wait for user input after command executed
        The wait flag has higher priority than :core:shell's `wait`
        configuration flag.
        """

        if kwargs.get("current", False):
            cmd = "./%s" % cmd

        if kwargs.get("bg", False):
            bg = ["&"]
        else:
            bg = []

        reloadp = kwargs.get("reload", True)
        wait = kwargs.get("wait", None)

        try:
            exef = cls.xyz.pm.from_load(":core:shell", "execute")
            escapef = cls.xyz.pm.from_load(":sys:cmd", "escape")
            reloadf = cls.xyz.pm.from_load(":sys:panel", "reload_all")
            exef(" ".join([escapef(cmd, True)] +
                          [escapef(a, True) for a in args] + bg), wait=wait)
            if reloadp:
                reloadf()
        except Exception, e:
            error(_(u"Error in DSL shell execution: %s") % unicode(e))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def alias(cls, alias, replace):
        """
        Set an alias which will be expanded in command line before execution
        @param replace: Either string or function
        """

        return cls.let(alias, replace, sect="aliases")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def icmd(cls, command, obj):
        """
        Set an internal command.
        """

        if not is_func(obj):
            error(_(u"Invalid object type: %s. Function expected") %
                  type(obj), trace=False)

        return cls.let(command, obj, sect="commands")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def plugins_on(cls, *plugins):
        """
        Enable plugin[s]
        """

        for plugin in plugins:
            cls.let("plugins", {plugin: "ENABLE"}, sect="xyz")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def plugins_off(cls, *plugins):
        """
        Disable plugin[s]
        """

        for plugin in plugins:
            cls.let("plugins", {plugin: "DISABLE"}, sect="xyz")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def plugin_conf(cls, plugin, opts):
        """
        Configure plugin.

        @param plugin: Plugin name
        @param opts: dict {var1: val1, var2: var2,..}
        """

        if not isinstance(opts, dict):
            error(_(u"Invalid opts type: %s. Dict instance expected")
                  % type(opts))

        return cls.let(plugin, opts, sect="plugins")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def prefix(cls, shortcut):
        """
        Set new prefix key
        """

        cls.xyz.km.set_prefix(shortcut)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def help(cls, obj=None):
        """
        Help
        """

        fmt = lambda o: "%s\t%s" % (o, getattr(cls, o).__doc__)

        if obj is not None and obj not in cls.api:
            error(_(u"Invalid function %s") % obj)

        if obj:
            objs = [obj]
        else:
            objs = cls.api

        return "\n".join([fmt(x) for x in objs]).replace("\t", " ")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def vfs(cls, prefix, vfsclass):
        """
        Set prefix and VFSObject class for VFS dispatching
        """

        try:
            return cls.xyz.vfs.register(prefix, vfsclass)
        except Exception, e:
            error(_(u"Error setting VFS prefix: %s") % unicode(e))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def vfs_path(cls, path, driver):
        """
        Construct path using provided VFS driver
        """

        return path + "#vfs-%s#" % driver

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def hook(cls, event, proc):
        """
        Register a new hook.
        Event is an event string and proc is a procedure to be called
        """

        try:
            return cls.xyz.hm.register(event, proc)
        except Exception, e:
            error(_(u"Error registering new hook: %s") % unicode(e))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def unhook(cls, event):
        """
        Remove all hooks for the event
        """

        return cls.xyz.hm.clear(event)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def fsrule(cls, rule):
        """
        Return libxyz.core.FSRule instance
        """

        try:
            return FSRule(rule)
        except Exception, e:
            error(_(u"Error parsing FSRule: %s") % unicode(e))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def palette(cls, config):
        """
        Create internal palette object

        @param config: Dictionary of form:
        {
           'foreground': COLOR,
           'background': COLOR,
           'fg_attributes': [ATTR],
           'mono': [ATTR],
           'foreground_high': HG_COLOR,
           'background_high': HG_COLOR
        }
        """

        try:
            return Palette(None, *Palette.convert(config))
        except Exception, e:
            error(_(u"Error creating Palette instance: %s") % unicode(e))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def skin(cls, **kwargs):
        """
        Make and register new skin
        """

        try:
            cls.xyz.sm.add(Skin(**kwargs))
        except Exception, e:
            error(_(u"Error creating Skin instance: %s") % unicode(e))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def execute(cls, source):
        """
        Execute DSL statements
        @param source: Either string or open file-object or code object
        """

        try:
            exec source in cls._env.copy()
        except Exception, e:
            error(_(u"Error in DSL execution: %s") % unicode(e))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    @instantiated
    def get_env(cls):
        """
        Return copy of global dsl environment
        """

        return cls._env.copy()

#++++++++++++++++++++++++++++++++++++++++++++++++

## Auto-generate corresponding module-level functions
module = sys.modules[__name__]

__all__ = ["XYZ"]

for f in XYZ.api:
    setattr(module, f, getattr(XYZ, f))
    __all__.append(f)
