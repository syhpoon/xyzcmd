=======
Plugins
=======

Plugins are the primary way to extend |XYZ| functionality.
In fact even base functionality is implemented mainly via plugins.

Plugins are being held in one of the following directories:

- System plugins: subdirectory of main |XYZ| installation path 
  (usually /usr/local/share/xyzcmd/plugins). All base system plugins are held
  here.
- User plugins: Any other third-party plugins are held in ~/.xyzcmd/plugins.

In these directories namespace subdirectories are created (see below for
more details).

Plugin entry-point is a main.py file inside plugin directory.
This file should contain class named ``XYZPlugin`` sublclassed from 
libxyz.core.plugins.BasePlugin class.

XYZPlugin class should define following mandatory attributes:

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

Also some optional attributes can be defined:

**MIN_XYZ_VERSION**
   Minimal |XYZ| version the plugin can be used with.
   If none defined, plugin will be available to use with any |XYZ| version.

Namespaces
----------
Namespaces are used to hierarchically organize exported methods and
to prevent method-names collisions. Namespace path can be specified
either in absolute or in minimal form.

Typical absolute namespace path is::

   xyz:plugins:<namespace>:<plugin-name>

Minimal path can be specified as following::
   
   :<namespace>:<plugin-name>

Here ``<namespace>`` is one of the available namespaces::

   - ui    - User-interface related
   - vfs   - Virtual file-system related
   - misc  - Other miscellaneous

Plugin exports its public methods via 'public' dictionary of BasePlugin class.

Managment
---------
All plugin management is performed using PluginManger instance, accessible as 
``pm`` attribute of ``libxyz.core.XYZData`` object named ``xyz``.

PluginManger supports two main procedures:
   
**load <plugin>**
   Search for <plugin>, load it, instanciate, prepare (run prepare()) and return

**from <plugin> load <method>**
   Load public method <method> from <plugin>.

In both cases <plugin> is a plugin namespace path.
