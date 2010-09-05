.. include:: includes.inc

================
Events and hooks
================

|XYZ| uses mechanism of events to notify parts of the system about
workflow and hooks system to handle the events.

Main characters in this play are event, hook, hooks manager

Event
-----
Event is fired by different parts of the system, mainly plugins,
when some pre-defined action is about to occur.
Event is represented by a string. When fired from the plugins it has form:
`event:<plugin>:<path>:<event_name>`. An event can carry zero or
more arguments along with it.

For example, before passing a typed command to shell, method
`:core:shell:execute` fires an event `event:core:shell:execute` with typed
command as an argument.

Hooks manager
-------------
Hooks manager is an internal events dispatcher. Its main purpose is to
call user-defined hooks, when an event occurs.

Hook
----
Hook is a user-defined action to be performed when an event occurs. A
hook can be established by calling HookManager instance's (xyz.hm)
:func:`register` method, or by using hook() function in configs.

System events
-------------
List of events fired by core system:

**event:startup**
  Event is fired after |XYZ| initialization is done.

  Arguments: no

**event:shutdown**
  Event is fired before |XYZ| shuts down.

  Arguments: no

**event:plugin_init**
  Event is fired when plugin is about to be loaded.

  Arguments: Namespace instance

**event:plugin_prepare**
  Event is fired before calling plugin prepare() method.

  Arguments: Plugin instance

**event:plugin_from_load**
  Event is fired when a plugin method is about to be loaded.

  Arguments: Plugin Namespace instance, and method name.

**event:plugin_from_load_data**
  Event is fired when a data object is about to be loaded.

  Arguments: Plugin Namespace instance, an object name.

**event:plugin_fin**
  Event is fired when plugin is shutting down.

  Arguments: Plugin instance

**event:conf_update**
  Event is fired when configuration parameter is changed via let() function.

  Arguments: Variable, Value, Section

Plugins events
--------------
List of events fired by standard plugins:

:core:bindlist
~~~~~~~~~~~~~~
**event:core:bindlist:show_binds**
  Event is fired before showing dialog.

  Arguments: no

:core:console
~~~~~~~~~~~~~
**event:core:console:show**
  Fires upon showing console window.

  Arguments: no

**event:core:console:cmd_prev**
  Fires when scrolling through history.

  Arguments: Current command from history buffer

**event:core:console:execute**
  Fires when typed command is to be executed.

  Arguments: Typed command

:core:keycodes
~~~~~~~~~~~~~~
**event:core:keycodes:show**
  Fires upon showing dialog.

  Arguments: no

:core:pluginlist:
~~~~~~~~~~~~~~~~~
**event:core:pluginlist:show**
  Fires upon showing dialog.

  Arguments: no

**event:core:pluginlist:info**
  Fires when showing detailed plugin info.

  Arguments: Selected plugin object

:sys:panel
~~~~~~~~~~
**event:sys:panel:before_switch_tab**
  Fires before switching to another tab.

  Arguments: Block instance, Old tab index

**event:sys:panel:switch_tab**
  Fires when switching to another tab.

  Arguments: Block instance, New tab index

**event:sys:panel:new_tab**
  Fires when new tab is added.

  Arguments: Block instance, New tab index

**event:sys:panel:del_tab**
  Fires when tab is delete.

  Arguments: Block instance, Deleted tab index

:core:shell
~~~~~~~~~~~
**event:core:shell:execute**
  Fires before command execution.

  Arguments: A command string to be executed

:vfs:fileinfo
~~~~~~~~~~~~~
**event:vfs:fileinfo:fileinfo**
  Fires upon showing file-info dialog.

  Arguments: Currently selected VFSObject instance
