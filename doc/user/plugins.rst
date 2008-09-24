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
:class:`libxyz.core.plugins.BasePlugin` class.

XYZPlugin class should define following mandatory attributes:

**NAME**
   Plugin name.

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

**DOC**
   Plugin documentation. Usually configuration variables described here.

**HOMEPAGE**
   Plugin home-page

Namespaces
----------
Namespaces are used to hierarchically organize exported methods and
to prevent method-names collisions.

Typical plugin namespace path is::

   :<namespace>:<plugin-name>

Here ``<namespace>`` is one of the available namespaces::

   - sys   - Virtual system plugins
   - core  - Core plugins
   - ui    - User-interface related
   - vfs   - Virtual file-system related
   - misc  - Other miscellaneous

Managment
---------
All plugin management is performed using PluginManger instance, accessible as 
``pm`` attribute of :class:`libxyz.core.XYZData` object named ``xyz``.

PluginManger supports following methods:
   
**load(<plugin>)**
   Search for <plugin>, load it, instantiate, prepare (run prepare()) and return

**reload(<plugin>)**
   Force [re]loading <plugin> even if it is already stored in cache.

**from_load(<plugin>, <method>)**
   Load public method <method> from <plugin>.

**from_load_data(<plugin>, <obj>)**
   Load public data <obj> from <plugin>.

In all cases <plugin> is a plugin namespace path.

Once loaded plugin is stored in cache, so subsequent calls will simply return
it from cache. If reloading needed ``reload`` method is used.

Lifecycle
---------
Only enabled plugins can be loaded and used. List of enabled plugins must
be defined in `xyz configuration file`_. Plugins are usually loaded by
first request. 

After plugin gets loaded for first time following actions take place:

- An instance of XYZPlugin class created 
- A prepare() method is run

Plugin can export methods and data.

Plugin exports its public methods via 'public' dictionary of BasePlugin class.
Access to public methods can be performed as:

   - ``plugin.public["method"]()``
   - ``plugin.method()``

Second variant is simpler, cleaner and therefore preferable.

Plugin exports its public data via 'public_data' dictionary of BasePlugin class.
Access to public data can be performed as:

   - ``plugin.public_data["obj"]``
   - ``plugin["obj"]``

So, in general, access to public methods is performed as attribute access:
``plugin.method()``, and access to public data is performed as dict-item access:
``plugin["data_obj"]``.

Following is an example of typical plugin usage in python code
(other cases will be described later)::

   # Load plugin
   hello = self.xyz.pm.load(":misc:hello")

   # Call public method say_hello() directly
   hello.say_hello()

   # Access public data `some_object`
   print hello["some_object"]

   # Or load only the method itself using from_load
   say_hello = self.xyz.pm.from_load(":misc:hello", "say_hello")

   # And then call
   say_hello()

   # Load only the data object itself using from_load_data
   some_object = self.xyz.pm.from_load_data(":misc:hello", "some_object")

Also see the `keys configuration file`_ for how to bind plugin methods to
keyboard shortcuts.

Configuration
-------------
All the neccessary plugin configuration provided via ``plugins``
configuration file. Its syntax is simple::

 <:plugin:ns:path> {
   var = val
   ...
 }

So single block contains configuration for one plugin.
Value can be of any common types recognized by lexer. See developer's manual,
chapter *Parsers*.

For example, if we'd have following block in plugins config::

   :misc:hello {
      show_version = true
   }

Plugin :misc:hello can access ``show_version`` variable as::

   show_version = xyz.conf[u"plugins"][u":misc:hello"][u"show_version"]

Virtual plugins
---------------
**TODO**
