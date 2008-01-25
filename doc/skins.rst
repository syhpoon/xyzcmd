=====
Skins
=====

Skins are used to configure visual representation of XYZ Commander.
Customizable elements are:

* Elements of filesystem based on:
   - file types
   - file permission bits
   - file owner
   - regular expressions
* All user interface widgets

Skin-definition file is a plain-text file containing skin-directives.
Every skin has a name. Name of the file which holds skin definition
is also a skin name.
Skin-files may be located in skins subdirectory of xyzcmd main installation
path or in user .xyz/skin directory.

Variables
---------

Variables could be defined and used within skin file.
New variable definition syntax is:
   ``set variable value``
Variable name is any alphanumeric character plus "_".
TODO: Value syntax

There are three mandatory variables to be defined in every skin 
and as much as necessary optional/local variables.
To access variable's value use following construction:
   ``%{variable}``

These are mandatory variables:
author
   Skin author name. Preferably in format: Name <author@foo.bar>

version
   Skin version

description
   Some skin description

Types
-----

File object can be highlighted depending on its type.
Possible types:

* file       - regular file
* block      - block special file
* char       - character special file
* dir        - directory
* link       - symbolic link
* fifo       - FIFO
* socket     - socket

General ruleset definition syntax::
   FS <by> {
      <fstype> = <FG>,[,<BG>][,<MA>]
      ...
   }

``FS`` means that we're defining file-system object[s].
``<by>`` means that we want to highlight by file type.
``<by>`` can take following values:

   * type     - File type
   * perm     - Permission bits
   * owner    - Owner
   * regexp   - Regular expression

``<fstype> = <FG>,[,<BG>][,<MA>]`` is a definition of object visual
representation.
<FG> 
   Foreground color. Possible values include:

      * BLACK
      * BROWN
      * YELLOW
      * WHITE
      * DEFAULT
      * DARK_BLUE
      * DARK_MAGENTA
      * DARK_CYAN
      * DARK_RED
      * DARK_GREEN
      * DARK_GRAY
      * LIGHT_GRAY
      * LIGHT_RED
      * LIGHT_GREEN
      * LIGHT_BLUE
      * LIGHT_MAGENTA
      * LIGHT_CYAN

<BG>
   Background color. Possible values include:

      * BLACK = 'black'
      * BROWN
      * DEFAULT
      * DARK_RED
      * DARK_GREEN
      * DARK_BLUE
      * DARK_MAGENTA
      * DARK_CYAN
      * LIGHT_CYAN

<MA>
   Monochrome terminal attributes. Possible values include:

      * BOLD
      * UNDERLINE
      * STANDOUT
      * DEFAULT

Example::

   FS type {
      file = LIGHT_GRAY
      dir = WHITE
      block = DARK_MAGENTA
      char = LIGHT_MAGENTA
      link = LIGHT_CYAN
      fifo = DARK_CYAN
      socket = DARK_RED
   }

Here ``file = LIGHT_GRAY`` means that all regular files (if not covered by
other rulesets) will appear in LIGHT_GRAY color.

Permission bits can be specified in following formats:

   * dddd - an absolute mode in octal number.
   * [+-]rwx - TODO: like in find -perm

   FS perm {
      4000 = LIGHT_RED
      +x = LIGHT_GREEN
   }

   FS owner {
      root:wheel = LIGHT_RED
   }

Here we define that all files owned by root will be displayed
in LIGHT_RED color.

Serching for rule in ruleset continues until first match is found.

Applying rules priorities:
   1. By owner
   #. By permission
   #. By regular expression
   #. By file-type
