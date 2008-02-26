=======
Plugins
=======

Plugins are the primary way to extend |XYZ| functionality.
In fact even base functionality is implemented mainly via plugins.

Plugins are being held in one of two directories:

- System plugins: subdirectory of main |XYZ| installation path 
  (usually /usr/local/share/xyzcmd/plugins). All base system plugins are held
  here.
- User plugins: Any other per-user plugins are held in ~/.xyzcmd/plugins.

For every installed plugin a directory created in an appropriate path with name
matching plugin-name.

Plugins usually contain a bunch of files:

- meta_:              Plugin meta-information. Mandatory.
- conf:              Plugin configuration. Optional.
- <pluginname>.py:   Main plugin file. Mandatory.
- any other needed files...

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

All of these variables are required to be defined in meta-file.

Namespaces
----------
Namespaces are used to hierarchically organize exported methods and
to prevent method-names collisions.
