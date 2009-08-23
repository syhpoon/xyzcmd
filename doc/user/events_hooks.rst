.. include:: includes.inc

================
Events and hooks
================

|XYZ| uses mechanism of events to notify parts of the system about
 workflow and hooks system to handle the events.

Main characters in this play are:

Event
-----
Event is fired by different parts of the system, mainly plugins,
when some pre-defined action is about to occur.
Event is a string. When fired from the plugins it has form:
`event:<plugin>:<path>:<event_name>`. An event can carry zero or
more arguments along with it.

For example, before passing a typed command to shell, method
`:sys:cmd:execute` fires an event `event:sys:cmd:execute` with typed
string as an argument.

Hook manager
------------
Hook manager is an internal events dispatcher. Its main purpose is to
call user-defined hooks, when an event occurs.

Hook
----
Hook is a user-defined action to be performed when an event occurs. A
hook can be established by calling HookManager instance's (xyz.hm)
:func:`register` method, or by using hook() function in configs.
