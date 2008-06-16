===================
Configuration files
===================

keys
----
``keys`` configuration file is used to bind methods, exported by plugins
to keyboard shortcuts.

File syntax is following:

* ``#`` Begins commentary to the end of line
* ``load {plugin_path}`` loads plugin
* ``bind[!] {method} to {shortcut} [context {contextname}]`` binds method 
  to be invoked upon pressing shortcut in context.
  If shortcut is already binded do nothing unless ``!`` flag is specified.
* ``set chain key {shortcut} [context {contextname}]`` set chain key
  for context or for DEFAULT unless provided

Where:

**{plugin_path}**
   Absolute or minimal plugin namespace path.
   For example: ``xyz:plugins:misc:hello`` or ``:misc:hello``

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
   bind META-P to default_action
   # 2.
   bind META-P to box_action context BOX

In 1. we've bound Meta+Shift+p shortcut to default_action method. As we haven't
provided context name, **DEFAULT** will be used.

In 2. we've explicitly provided **BOX** context. So box_action will only
be executed when a widget with context **BOX** will be in focus
receiving input.

To make a widget belonging to some context, a *context* keyword should be
passed to constructor.

Shortcut chains
+++++++++++++++
In general, shortcut will contain two keys: modifier (like META or CTRL) and
the regular key. As only widget receives such a combination, it tries to
search among defined shortcuts to determine what action to fire.
But we can tell |XYZ| not to immediately look for action by providing
a ``chain key``, which will indicate beginning of multiple shortcuts
combination treated as single one.

To bind a chain key we use the following syntax
``set chain key {shortcut} [context {contextname}]``.

So, if we have::

   set chain key CTRL-j
   set chain key META-G context BOX

Pressing CTRL-j in default context would not trigger action lookup, but instead
KeyManager will wait for next shortcut in chain until the same chain key
pressed again or timeout reached.
Thus, pressing ``CTRL-j META-1`` in ``BOX`` context will trigger
KeyManager to lookup for shortcut ``CTRL-j META-1``.

xyz
----
**TODO**
