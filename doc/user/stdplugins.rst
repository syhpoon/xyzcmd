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
**TODO**

``:vfs:`` plugins
-----------------
**TODO**

``:misc:`` plugins
------------------
**TODO**

``:sys:`` plugins
-----------------
**TODO**
