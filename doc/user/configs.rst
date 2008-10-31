===================
Configuration files
===================

|XYZ| uses the two-layered scheme for configuration files:

*System configuration files*
   |XYZ| relies on system configuration files to perform a 
   correct initialization as almost all default values are kept in those
   configs and not hardcoded in |XYZ| itself. |XYZ| looks for
   system configs in the main installation directory (usualy
   :file:`/usr/local/share/xyzcmd` or :file:`/usr/share/xyzcmd`).
   System configs aren't supposed to be edited.

*User configuration files*
   All configuration is done in user configs. They can be held in user home
   dir: :file:`~/.xyzcmd`. So if you need to make any change - just copy
   corresponding config from system configs or create an empty one and make
   all the neccessary changes.

At startup |XYZ| first reads default values from system configs and
then tries to open and parse user's ones.

keys
----
``keys`` configuration file is used to bind methods, exported by plugins
to keyboard shortcuts.

File syntax is following:

* ``#`` Begins commentary to the end of line
* ``load {plugin_path}`` loads plugin
* ``bind {method} to {shortcut} [context {contextname}]`` binds method 
  to be invoked upon pressing shortcut in context.

Where:

**{plugin_path}**
   Plugin namespace path.
   For example: ``:misc:hello``

**{method}**
   Plugin exported method.

**{shortcut}**
   A keyboard shortcut. See Shortcuts_ below.

**{contextname}**
   Running context. See Contexts_ below.

Shortcuts
+++++++++
Shortcut is a combination of keys pressed.
It is specifed as a list of special (libxyz.ui.Keys attributes) and
regular keys separated by hiphen::

   CTRL-x  means Control + x key
   META-L  means Escape + SHIFT + l key

.. note::
   Please note that not all of the possible combinations make sense.

There is a standard plugin ``:ui:testinput`` which can be usefull to determine
what kind of shortcuts are corresponding to pressed keys.

Contexts
++++++++
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
   bind :sys:cmd:undo to META-P
   # 2.
   bind :sys:cmd:undo to META-P context CMD

In 1. we've bound Meta+Shift+p shortcut to undo method of :sys:cmd plugin.
As we haven't provided context name, **DEFAULT** will be used.

In 2. we've explicitly provided **CMD** context. So box_action will only
be executed when a widget with context **CMD** will be in focus
receiving input.

One can provide a special context name: ``@`` to make context name equal to
plugin full namespace path::

   bind :sys:cmd:execute to ENTER context @

In this case, the bind will be saved to context ``:sys:cmd``.

xyz
----
**TODO**
