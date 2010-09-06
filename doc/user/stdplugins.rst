.. include:: includes.inc

================
Standard plugins
================
This chapter contains a list and description of all standard plugins, shipped
with |XYZ|.

``:core: plugins``
------------------
*:core:* plugins provide, well, core functionality. As it was stated before,
main part of |XYZ| functionality provided in plugins, thus keeping
a base |XYZ| part lightweight, simple and clean.

Here is the list of standard *:core:* plugins:

* :ref:`:core:bindlist <core-bindlist>`
* :ref:`:core:console <core-console>`
* :ref:`:core:keycodes <core-keycodes>`
* :ref:`:core:pluginlist <core-pluginlist>`
* :ref:`:core:shell <core-shell>`
* :ref:`:core:complete <core-complete>`

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

Events:

**event:core:bindlist:show_binds**
  Event is fired before showing dialog.

  Arguments: no.

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

.. _core-complete:

``:core:complete``
++++++++++++++++++
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
VFS plugins are used to extend and simplify things with VFS subsystem.

List of standard *:vfs:* plugins:

* :ref:`:vfs:fileinfo <vfs-fileinfo>`
* :ref:`:vfs:vfsutils <vfs-vfsutils>`

.. _vfs-fileinfo:

``:vfs-fileinfo``
+++++++++++++++++
Dialog showing detailed information provided by VFS layer.

Public methods:

**fileinfo()**
  Show dialog with information on selected VFS object.

.. _vfs-vfsutils:

``:vfs:vfsutils``
+++++++++++++++++
Plugins contains bunch of useful VFS utils.

Public methods:

**copy(move=False)**
  Show copy dialog.
  move: If move is True - move objects instead of just copying.

**mkdir()**
  Create new directory dialog.

**move()**
  Show move dialog (a shorthand for copy(move=True)).

**remove()**
  Show remove dialog.

``:misc:`` plugins
------------------
Misc plugins contains some other miscellaneous utilites that just
don't fit into other plugin categories.

``:misc:about``
+++++++++++++++
About |XYZ| plugin.

Public methods:

**about()**
  Show about panel.

``:misc:where``
+++++++++++++++
Plugin is used to save/restore navigation state of |XYZ|.
It saves/restores all tabs opened on both panels as well selected files
in each tab too.

Public methods:

**load()**
  Restore navigation state. It is called by handler bound to
  :ref:`:event:startup <system-events>`.

**save()**
  Save navigation state. It is called bu handler bound to
  :ref:`:event:shutdown <system-events>`.

``:sys:`` plugins
-----------------
*:sys:* plugins don't really exist as a separate entity in :file:`plugins`
directory. Instead they are constructed inside running |XYZ| modules.
They're kind of "virtual" plugins, but nevertheless they play a
significant roles in overall system behaviour.


``:sys:panel``
++++++++++++++
This plugin is a "face" of |XYZ|, it is responsible for drawing both navigation
panels and interact with user.

Public methods:

**action(active=True)**
  Perfrom a defined action (if any) on selected object.

  active: If True performs on active panel, otherwise - on inactive one.

**active_tab(active=True)**
  Get active tab index.

  active: If True performs on active panel, otherwise - on inactive one.

**block_next()**
  Jump to the next block of objects.

**block_prev()**
  Jump to the previous block of objects.

**chdir(path,active=True)**
  Change directory. The directory can be in a full |XYZ| VFS format.

  path: VFS path.
  active: If True performs on active panel, otherwise - on inactive one.

**cwd(active=True)**
  Get current working directory.

  active: If True performs on active panel, otherwise - on inactive one.

**del_tab(index=None,active=True)**
  Delete tab. If index is None - delete current tab.

  active: If True performs on active panel, otherwise - on inactive one.

**entry_bottom()**
  Jump to the bottom object.

**entry_next()**
  Jump to the next object.

**entry_prev()**
  Jump to the previous object.

**entry_top()**
  Jump to the topmost object.

Events:

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

``:sys:cmd``
++++++++++++

