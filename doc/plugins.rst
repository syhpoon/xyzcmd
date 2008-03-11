=======
Plugins
=======

Plugins are the primary way to extend |XYZ| functionality.
In fact even base functionality is implemented mainly via plugins.

Plugins are being held in one of two directories:

- System plugins: subdirectory of main |XYZ| installation path 
  (usually /usr/local/share/xyzcmd/plugins). All base system plugins are held
  here.
- User plugins: Any other third-party plugins are held in ~/.xyzcmd/plugins.

For every installed plugin a directory created in an appropriate path with name
matching plugin-name.

Plugins usually contain following files:

- meta_:             Plugin meta-information. Mandatory.
- conf:              Plugin configuration. Optional.
- <pluginname>.py:   Main plugin file. Mandatory.
- any other needed files... Optional.

.. _meta:

Meta-information
----------------
File 'meta' contains important plugin information.
File syntax is simple: ``value: variable``
Here is a full list of available variables:

**AUTHOR**
   Plugin author name. Preferably in format ``Name <foo@bar>``.

**VERSION**
   Plugin version.

**BRIEF_DESCRIPTION**
   Brief one-line plugin description.

**FULL_DESCRIPTION**
   Full plugin description. Put anything here.

**NAMESPACE**
   Plugin namespace. See Namespaces_

All these variables are mandatory.
Also some optional variables can be defined:

**MIN_XYZ_VERSION**
   Minimal |XYZ| version the plugin can be used with.
   If none defined, plugin will be available to use with any |XYZ| version.

Namespaces
----------
Namespaces are used to hierarchically organize exported methods and
to prevent method-names collisions. Стоит обратить внимание на то, что
иерархический путь плагина это не то-же самое что путь к python-модулю
его реализующему.
Типичный полный путь плагина выглядит так:
``xyz:plugins:<namespace>:<plugin-name>``

Здесь ``<namespace>`` - один из доступных типов плагина.
Доступны следующие типы:

-- 
Every single plugin should inherit libxyz.core.BasePlugin interface.
Plugin exports its public methods via 'public' dictionary of BasePlugin class.
Plugin must be registered within one of xyz plugin namespaces.
Available namespaces are:
- ui    - User-interface related
- vfs   - Virtual file-system related
- misc  - Other miscellaneous
