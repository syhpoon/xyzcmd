.. include:: includes.inc

================
Standard plugins
================
This chapter contains a list and description of all standard plugins, shipped
with |XYZ|.

``:core: plugins``
------------------
*:core:* plugins provide, well, core functionality. As it was stated before,
main part of |XYZ| functionality provided via plugins, thus keeping
a base |XYZ| part lightweight, simple and clean.

Here is the list of standard *:core:* plugins:

* :ref:`:core:bindlist <core-bindlist>`
* :ref:`:core:console <core-console>`
* :ref:`:core:keycodes <core-keycodes>`
* :ref:`:core:pluginlist <core-pluginlist>`
* :ref:`:core:shell <core-shell>`

.. _core-bindlist:

``:core:bindlist``
++++++++++++++++++
Plugin is used to display all current keybindings along with corresponding
contextes and methods.

Public methods:

**show_binds()**
   The output list has three columns: *Context*, *Bind* and *Method*.
   *Context* columns contains context which was used upon binding.
   *Bind* colums contains keybinding and *Method* columns contains full method 
   name.

.. _core-console:

``:core:console``
+++++++++++++++++
Management console is used to manage |XYZ| in runtime.

Public methods:

**show()**
  Show console.

Events:

**event:core:console:show**
  Fires upon showing console.
  Arguments: No

**event:core:console:cmd_prev**
  Fires when scrolling through history.
  Arguments: Current command from history buffer.

**event:core:console:execute**
  Fires when typed command is to be executed.
  Arguments: typed command.

.. _core-keycodes:

``:core:keycodes``
++++++++++++++++++
KeyCodes plugin is used to properly configure terminal keycodes.
For each terminal type keycodes are stored independently.
Terminal type determined by examining *TERM* environment variable.

Learned data is stored in :file:`~/.xyzcmd/data/keycodes` file.

Public methods:

**learn_keys()**
   Shows LearnKeys dialog where user prompted to press required keys.
   *ENTER* - skip current key.
   *ESCAPE* - quit dialog.

**delete_keys(all=False)**
   Delete learned keycodes data.
   If all is True, delete all saved data for all terminal types,
   otherwise delete only current terminal type data.

**get_keys(all=False)**
   Return saved keycodes data as dictionary.
   If all is True, return all saved data for all terminal types,
   otherwise return only current terminal type data.

Events:

**event:core:keycodes:show**
  Fires upon showing dialog.

.. _core-pluginlist:

``:core:pluginlist``
++++++++++++++++++++
PluginList plugin is used to display a list of all currently active
plugins.

Public methods:

**show_list()**
   Show a list of all active plugins. All the list elements are browseble,
   i.e. pressing `ENTER` will bring a detailed plugin information, including
   full plugin description, version, available configuration variables
   and all the public methods and data.

Events:

**event:core:pluginlist:show**
  Fires upon showing dialog. Arguments: No.

**event:core:pluginlist:info**
  Fires when showing detaild plugin info.
  Arguments: Plugin object.

.. _core-shell:

``:core:shell``
+++++++++++++++
Plugin allows to execute commands by spawning external shell.

Public methods:

**execute(cmd, wait=None)**
  Execute command in shell.
  If wait flag is set, the user will be prompted to press key upon command
  execution completed, otherwise it will immediately return to |XYZ|.

**echo(msg)**
  Echo a message to terminal output.

*:core:shell* plugin provides additional configuration, based on user's
shell. For example, for bash it tries to import all aliases into |XYZ| 's
own aliases subsystem, making them available from inside |XYZ|.

Configuration options:

**wait**
  Boolean flag indicating whether to wait for user pressing
  key after command executed. Default True.

**setup_shell**
  Boolean flag indicating whether to run system shell-specific initialization.
  Default True.

Events:

**event:core:shell:execute**
  Fires before command execution.
  Arguments: a command to be executed

``:ui:`` plugins
----------------
UI plugins usually provide new UI widgets and functionality related to
ui subsystem in general.

List of standard *:ui:* plugins:

* :ref:`:ui:bookmarks <ui-bookmarks>`
* :ref:`:ui:testinput <ui-testinput>`

.. _ui-bookmarks:

``:ui:bookmarks``
+++++++++++++++++
Plugin is used to handle frequently used directories bookmarks.

Public methods:

**add_bookmark(path, name=None)**
   Add new bookmark entry.
   If name is not specified, path is used instead

**del_bookmark(name)**
  Delete saved bookmark entry by name.

**get_path(name)**
  Get bookmark path by name.

**show_bookmarks()**
  Show saved bookmarks in popup dialog. One can navigate through the list
  by pressing *UP* and *DOWN* keys. Pressing *RETURN* on the entry causes
  |XYZ| to chdir to specified path in active panel.

  Entry number can be used to quickly select particular entry, just type the
  number and then press *RETURN*.

.. _ui-testinput:

``:ui:testinput``
+++++++++++++++++
Simple dialog to show pressed keys.
This can be useful when selecting appropriate keybind defined in keys.xyz file.

Public methods:

**show_box(use_wrap=True)**
  Show test_box dialog.
  use_wrap: Whether to use input wrapper which honours learned keys.

  Upon pressing any key the shortcut and raw key will be shown.
  Shortcut is what XYZCommander expects to see in configuration files.
  Raw is what low-level library emits to focus widget.

``:vfs:`` plugins
-----------------
**TODO**

``:misc:`` plugins
------------------
**TODO**

``:sys:`` plugins
-----------------
**TODO**
