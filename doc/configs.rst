===================
Configuration files
===================

keys
----
``keys`` configuration file is used to bind methods, exported by plugins
to keyboard shortcuts.

File syntax is following:

* ``#`` Begins commentary to the end of line
* ``from {plugin_path} load {method}`` loads method from plugin
* ``load {plugin_path}`` loads plugin
* ``bind {method} to {shortcut}`` binds method to be invoked upon pressing 
  shortcut. If shortcut is already binded do nothing.
* ``bind! {method} to {shortcut}`` binds method to shortcut. Override if
  already binded.

Where:

**{plugin_path}**
   Absolute or minimal plugin namespace path.
   For example: ``xyz:plugins:misc:hello`` or ``:misc:hello``

**{method}**
   Plugin exported method.

**{shortcut}**
   A keyboard shortcut. See Shortcuts_ for more detail.

Shortcuts
+++++++++
Shortcut is a combination of keys pressed.
It is specifed as a list of special (libxyz.ui.Keys attributes) and
regular keys separated by hiphen::

   CTRL-SHIFT-X  -- Control + Shift + X
   META-L        -- Escape + L

Please note that not all of the combinations make sense.
