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
path or in user .xyz/skins directory.

Constants
---------

There are three mandatory constants to be defined in every skin.

**AUTHOR**
   Skin author name. Preferably in format: Name <author@foo.bar>

**VERSION**
   Skin version

**DESCRIPTION**
   Some skin description

Constant defined using construction: ``<CONST>: VALUE``

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

   fs <by> {
      <fstype> = <FG>,[,<BG>][,<MA>]
      ...
   }

``fs`` means that we're defining file-system object[s].

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

   fs type {
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

**[+]dddd**
   Octal digit mode. If mode is preceeded by '+' this will
   match files with any of mode bits set. Otherwise it will
   match only files with exactly the same mode as given::

      # Permission-based highlighting
      fs perm {
         # This will highlight any set-uid file in LIGHT_RED
         +4000 = LIGHT_RED
         # Files with execution bits set
         +0111 = LIGHT_GREEN
         # Match only files with exactly set mode - 755
         0755 = DARK_GREEN
      }

Owner/group can be specified as ``[uid][:gid]``. uid and gid both can be either
symbolic or numeric::

   fs owner {
      # Files owned by root and group wheel
      root:wheel = LIGHT_RED
      # Files owned by username
      username = WHITE
      # Files owned by group operator
      :operator = YELLOW
      # Files owner by user with uid 1050
      1050 = WHITE,DARK_RED
   }

Regular expressions based rules use filenames as match criteria.
Regular expression enclosed in ``//``. Character '=' must be escaped using 
``\`` backslash to prevent interpreting it as assign character::

   fs regexp {
      # Display .core files in DARK_RED
      /*.core$/ = DARK_RED
      # Hidden files
      /\.+/ = LIGHT_GREY
   }

Order
-----

Searching for rule in ruleset continues until first match is found
according to priorities.

Default rules priorities:
   1. By owner
   #. By permission
   #. By regular expression
   #. By file-type

So if we have following rulesets defined::

   fs perm { +0100 = DARK_RED }
   fs type { file = WHITE }
   fs owner { root = DARK_BLUE }

And if there is an executable file owned by root. It will be displayed using
DARK_BLUE, as owner rulesets have higher priority.

Priorities can be customized. This can be done using priority ruleset::

   fs priority {
      type = 1
      perm = 2
      regexp = 3
      owner = 4
   }
