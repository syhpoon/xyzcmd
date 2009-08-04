.. include:: includes.inc

===================
Configuration files
===================

|XYZ| uses the two-layered scheme for configuration files:

*System configuration files*
   |XYZ| relies on system configuration files to perform a 
   correct initialization as almost all default values are kept in those
   configs and not hardcoded in |XYZ| itself. |XYZ| looks for
   system configs in the main installation directory (usualy
   :file:`/usr/local/share/xyzcmd/conf` or :file:`/usr/share/xyzcmd/conf`).
   System configs aren't supposed to be edited by user.

*User configuration files*
   All configuration is done in user configs. They can be held in user home
   dir: :file:`~/.xyzcmd/conf`. So if you need to make any change - just copy
   corresponding config from system configs or create an empty one and make
   all the neccessary changes.

At startup |XYZ| first reads default values from system configs and
then tries to open and parse user's ones.

DSL
---
|XYZ| configuration files are, in fact, just regular python scripts
but in order to simplify configuration editing a bunch of useful
functions are available:

* :ref:`let <let>`
* :ref:`val <val>`
* :ref:`unlet <unlet>`
* :ref:`load <load>`
* :ref:`bind <bind>`
* :ref:`kbd <kbd>`
* :ref:`exec_file <exec_file>`
* :ref:`action <action>`
* :ref:`macro <macro>`
* :ref:`call <call>`
* :ref:`env <env>`
* :ref:`shell <shell>`
* :ref:`alias <alias>`
* :ref:`plugins_on <pluginson>`
* :ref:`plugins_off <pluginsoff>`
* :ref:`plugin_conf <pluginconf>`
* :ref:`icmd <icmd>`
* :ref:`prefix <prefix>`

.. _let:

let(variable, value, sect="local")
++++++++++++++++++++++++++++++++++
Set `variable` to hold a `value`.
Variable will be available in ``xyz.conf[section][varname]``
If section is not provided - `local` will be used.


Example - Choose a desired skin::

  let("skin", "seablue", sect="xyz")

.. _val:

val(variable, sect="local")
+++++++++++++++++++++++++++
Retrieve `variable` value.

Example::

  val("skin", sect="xyz")

.. _unlet:

unlet(variable, sect="local")
+++++++++++++++++++++++++++++
Delete `variable` binding if exists.

Example::

  unlet("myvar")

.. _load:

load(plugin)
++++++++++++
Load method[s] from `plugin`.

Example - load all methods from `:sys:cmd` plugin::

  load(":sys:cmd:*")

Example - load `show_binds` method from ``:core:bindlist`` plugin::

  load(":core:bindlist:show_binds")

.. _bind:

bind(method, shortcut, context="DEFAULT")
+++++++++++++++++++++++++++++++++++
Bind `method` to be executed upon pressing `shortcut`.
Method can be either full plugin method pass or python
function/method/lambda object.
If `context` is *@* - use plugin full path as context. (See :ref:`contexts`)

Example - run ``:sys:cmd:execute`` when `ENTER` is pressed::

  bind(":sys:cmd:execute", kbd("ENTER"))

Example - use system pager to view files::

  bind(lambda: shell(env("PAGER", "less"), macro("ACT_PATH")), kbd("F3"))

.. _kbd:

kbd(*args)
++++++++++
Transform a string shortcut description into internal representation
object.

Example::

  kbd("ENTER")

.. _exec_file:

exec_file(filename)
+++++++++++++++++++
Execute another configuration file

Example::

  exec_file("custom.xyz")

.. _action:

action(rule, fn)
++++++++++++++++
Set up an action to be taken upon pressing action key on file.
Action key is by default - `ENTER` which is bound to ``:core:panel:action``.

Example - when action is pressed on executable file - run it::

  action(r'(type{file} and perm{+0111}) or '\
         r'(type{link} and link_type{file} and link_perm{+0111})',
         lambda obj: shell(obj.path))

.. _macro:

macro(macroname)
++++++++++++++++
Expand macro name.

Availbale macros:

*ACT_CWD*
  Working directory in active panel

*INACT_CWD*
  Working directory in inactive panel

*ACT_PATH*
  Full selected object path in active panel

*INACT_PATH*
  Full selected object path in inactive panel

*ACT_BASE*
  Parent directory in active panel

*INACT_BASE*
  Parent directory in inactive panel

*ACT_TAGGED*
  List of tagged files in active panel

*INACT_TAGGED*
  List of tagged files in inactive panel

*ACT_UNTAGGED*
  List of not tagged files in active panel

*INACT_UNTAGGED*
  List of not tagged files in inactive panel

Example - edit current file::

  bind(lambda: shell(env("EDITOR", "vi"), macro("ACT_PATH")), kbd("F4"),
       ":sys:panel")

.. _call:

call(method, *args)
+++++++++++++++++++
Call plugin method passing arguments to it.

Example - change directory::

  action(r'type{dir} or (link_type{dir} and link_exists{?})',
         lambda obj: call(":sys:panel:chdir", obj.path))

.. _env:

env(variable, default=None)
+++++++++++++++++++++++++++
Return environment variable or default if is not set

Example::

  env("HOME", "/")

.. _shell:

shell(cmd, *args, **kwargs)
+++++++++++++++++++++++++++
Execute command using ``:core:shell`` plugin.

* Optional boolean argument `current` can be provided to indicate
  that cmd is to be run from current directory.

* Optional boolean argument `bg` can be provided to indicate that `cmd`
  must be executed in background.

* Optional boolean argument `reload` can be provided to indicate         
  that panel content should/should not be reloaded after execution.

Example - run `xpdf` in background on .pdf files::

  action(r'iname{".*\\.pdf$"}', lambda obj: shell("xpdf", obj.path, bg=True))

.. _alias:

alias(alias, replace)
+++++++++++++++++++++
Set an alias which will be expanded in command line before execution.
`replace` argument can be either string or function.

Example::

  alias("ll", "ls -l")

.. _icmd:

icmd(command, object)
+++++++++++++++++++++
Set an internal command. Internal command do not get passed to shell,
instead appropriate function is being called by |XYZ|.

Example::

  icmd("cd", lambda path: call(":sys:panel:chdir", path))

.. _pluginson:

plugins_on(*plugins)
++++++++++++++++++++
Enable plugin[s]. 

Example::

  plugins_on(":sys:run",
             ":sys:cmd",
             ":sys:panel",
             ":sys:logger")

.. _pluginsoff:

plugins_off(*plugins)
+++++++++++++++++++++
Disable plugin[s].

Example::

  plugins_off(":misc:about")

.. _pluginconf:

plugin_conf(plugin, opts)
+++++++++++
Configure plugin. 

Where:

* plugin: Plugin name

* opts: Either tuple (var, val) or dict {var1: val1, var2: var2,..}

In fact, ``plugin_conf`` is only a shortened form of ``let(plugin,
opts, sect="plugins")``.

Example::

  plugin_conf(":sys:cmd", ("prompt", "|| "))
  plugin_conf(":sys:cmd", {
              # Command line prompt
              "prompt": "$ ",
    
              # Size of undo buffer
              "undo_depth": 10,
    
              # Size of typed commands history buffer
              "history_depth": 50})

.. _prefix:

prefix(shortcut)
++++++++++++++++
Set new prefix key.

Example::

  prefix(kbd("CTRL-x"))

Files
-----
Although any |XYZ| configuration file can contain any (or all) of the
above functions, it is better to logically separate definitions.

Here's the list of |XYZ| system configuration files:

*actions.xyz*
  Contains action definitions.

*aliases.xyz*
  Contains aliases.

*icmd.xyz*
  Contains internal commands definitions.

*keys.xyz*
 ``keys`` configuration file is used to bind methods, exported by plugins
 to keyboard shortcuts.

*main.xyz*
  Main configuration files. Contains miscellaneous configuration
  directives.

*plugins.xyz*
  Plugins configuration.
 
Shortcuts
---------
Shortcut is a combination of keys pressed.
It is specifed as a list of special (libxyz.ui.Keys attributes) and
regular keys separated by hiphen::

   CTRL-x  means Control + x key
   META-L  means Escape + SHIFT + l key

.. note::
   Please note that not all of the possible combinations make sense.

There is a standard plugin ``:ui:testinput`` which can be usefull to determine
what kind of shortcuts are corresponding to pressed keys.

.. _contexts:

Contexts
--------
When a focus widget receives keyboard input it looks for matching key pressed
in KeyManager object accessible as ``km`` attribute of ``XYZData`` class.

But for different widgets the same keys/shortcuts can have different meanings.
For intance key *UP* pressed while Panel widget is active will move the
cursor one entry up. But for ``BoxYesNo`` dialog the same key changes the 
button focus.
To handle such a problem a concept of *context* is introduced.
Context is simply a set which shares the shortcuts defined within it.
Context has a name and may include an arbritrary amount of widgets.
Context named **DEFAULT** used unless other provided.
For example, consider the part of keys configuration file::

   # 1.
   bind(":sys:cmd:undo", kbd("META-P"))
   # 2.
   bind(":sys:cmd:undo", kbd("META-P"), "CMD")

In 1. we've bound Meta+Shift+p shortcut to undo method of :sys:cmd plugin.
As we haven't provided context name, **DEFAULT** will be used.

In 2. we've explicitly provided **CMD** context. So box_action will only
be executed when a widget with context **CMD** will be in focus
receiving input.

One can provide a special context name: ``@`` to make context name equal to
plugin full namespace path::

   bind(":sys:cmd:execute", kbd("ENTER"), "@")

In this case, the bind will be saved to context ``:sys:cmd``.
