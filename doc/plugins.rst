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

Plugins usually contain a bunch of files. Some of them are mandatory, some - 
optional::

- meta:              Plugin meta-information. Mandatory.
- conf:              Plugin configuration. Optional.
- <pluginname>.py:   Main plugin file. Mandatory.
- any other needed files...

Meta-information
----------------
