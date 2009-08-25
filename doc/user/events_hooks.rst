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
`:sys:cmd:execute` fires an event `event:sys:cmd:execute` with typed
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

  Arguments: Pluing Namespace instance, and method name.

**event:plugin_from_load_data**
  Event is fired when a data object is about to be loaded.

  Arguments: Plugin Namespace instance, an object name.

**event:plugin_fin**
  Event is fired when plugin is shutting down.

  Arguments: Plugin instance
