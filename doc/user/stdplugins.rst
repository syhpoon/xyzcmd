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

* :core:bindlist
* :core:console
* :core:keycodes
* :core:pluginlist

``:core:bindlist``
++++++++++++++++++
Plugin provides list of currently used keybindings.

Public methods:

**show_binds()**
   The output list has three columns: *Context*, *Bind* and *Method*.
   *Context* columns contains context which was used upon binding.
   *Bind* colums contains keybinding and *Method* columns contains full method 
   name.

``:core:console``
+++++++++++++++++
**TODO**

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

``:core:pluginlist``
++++++++++++++++++
PluginList plugin is used to display a list of all currently active
plugins.

Public methods:

**show_list()**
   Show a list of all active plugins. All the list elements are browseble,
   i.e. pressing `ENTER` will bring a detailed plugin information, including
   full plugin description, version, available configuration variables
   and all the public methods and data.

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
