=====
Skins
=====

Skins are used to configure visual representation of |XYZ|.
Customizable elements are:

* Elements of filesystem based on:
   - file types
   - file permission bits
   - file owner
   - regular expressions
* All user interface widgets

Skin-definition file is a plain-text file containing skin-directives.
Every skin has a name. Name of the file which holds skin definition
is a skin name.
Skin-files may be located in skins subdirectory of xyzcmd main installation
path or in user .xyz/skins directory.

.. note::
   For every palette defined in skin, a separate color pair is used, so
   keep in mind that a terminal has a limited number of available color pairs.
   And it's an error if you define too much of them.

Constants
---------

There are three mandatory constants to be defined in every skin.

**AUTHOR**
   Skin author name. Preferably in format: Name <author@foo.bar>

**VERSION**
   Skin version

**DESCRIPTION**
   Some skin description

Constants are defined using construction: ``<CONST>: VALUE``

Filesystem types
----------------

File object can be highlighted depending on its type.
Possible types:

* file       - regular file
* block      - block special file
* char       - character special file
* dir        - directory
* link       - symbolic link
* fifo       - FIFO
* socket     - socket

General fs ruleset definition syntax::

   fs.<by> {
      <var> = <FG>[,<BG>][,<MA1>[,<MA2>]...]
      ...
   }

``fs`` means that we're defining file-system ruleset.

``<by>`` means that we want to highlight some filesystem objects.

``<by>`` can take following values:

* type     - File type
* perm     - Permission bits
* owner    - Owner
* regexp   - Regular expression
* combined - Combinations of the aboe rules

``<var> = <FG>,[,<BG>][,<MA1>[,<MA2>,...]]`` is a definition of object visual
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

      * BLACK
      * BROWN
      * DEFAULT
      * DARK_RED
      * DARK_GREEN
      * DARK_BLUE
      * DARK_MAGENTA
      * DARK_CYAN
      * LIGHT_GRAY

<MA>
   Monochrome terminal attributes. Possible values include:

      * BOLD
      * UNDERLINE
      * STANDOUT
      * DEFAULT

   Monochrome attribute can hold more than one value.

fs.type
+++++++

Example::

   fs.type {
      file = LIGHT_GRAY
      dir = WHITE
      block = DARK_MAGENTA
      char = LIGHT_MAGENTA
      link = LIGHT_CYAN
      fifo = DARK_CYAN
      socket = DARK_RED,LIGHT_GRAY,BOLD,UNDERLINE
   }

Here ``file = LIGHT_GRAY`` means that all regular files (if not covered by
other rulesets) will appear in LIGHT_GRAY color.
``socket = DARK_RED,LIGHT_GRAY,BOLD,UNDERLINE`` means that socket objects
will appear in dark red text on light gray background using bold and underline
attributes.

fs.perm
+++++++

Permission bits can be specified in following formats:

**[+]dddd**
   Octal digit mode. If mode is preceeded by '+' this will
   match files with any of mode bits set. Otherwise it will
   match only files with exactly the same mode as given::

      # Permission-based highlighting
      fs.perm {
         # This will highlight any set-uid file in LIGHT_RED
         +4000 = LIGHT_RED
         # Files with execution bits set
         +0111 = LIGHT_GREEN
         # Match only files with exactly set mode - 755
         0755 = DARK_GREEN
      }

fs.owner
++++++++

Owner/group can be specified as ``[uid][:gid]``. uid and gid both can be either
symbolic or numeric::

   fs.owner {
      # Files owned by root and group wheel
      root:wheel = LIGHT_RED
      # Files owned by username
      username = WHITE
      # Files owned by group operator
      :operator = YELLOW
      # Files owner by user with uid 1050
      1050 = WHITE,DARK_RED
   }

fs.owner ruleset internal resolution order is following:
   1. ``uid:gid``
   #. ``uid``
   #. ``gid``

fs.regexp
+++++++++

Regular expressions based rules use filenames as match criteria.
Regular expressions must use x-quoting: ``'''<re>'''``::

   fs.regexp {
      # Display .core files in DARK_RED
      '''.+\.core$''' = DARK_RED
      # Hidden files
      '''\.+''' = LIGHT_GREY
   }

If the filename could be matched against two or more defined regexps,
system will pick up first of those in arbitrary order.

fs.combined
+++++++++++
All rulesets described above work fine in most simple cases.
But it is impossible to describe, say, combined logical rules.
For example we want to create a rule to highlight all regular files with
executable bit set.

That, the fs.combined ruleset is for. You can describe arbitrary complex 
logical expressions.
The format if following::

 fs.combined {
   "rule" = <ATTRS>
 }

Where ``<ATTRS>`` are the rule attributes in the same format as in the other
rulesets, and "rule" is a string expression.
General rule format is::

 [not] <ftype>{<arg>} [<op> ...]

Where ``<ftype>`` is a rule type, matching the names of fs.* rulesets.
``<arg>`` is an argument and ``<op>`` is a logical operator (and, or)
joining two or more expressions.
So, the example described above could be matched using rule::

   fs.combined {
      "type{file} and perm{+0111}" = WHITE, BLACK
   }

More complex rules can be split along several lines using x-quoted strings::

   fs.combined {
      '''
      type{dir} or type{file}
      and (owner{user} or owner{root})
      and perm{+4000}
      ''' = DARK_RED, BLACK
      }

In fact, using fs.combined ruleset you can match any supported combination
of VFS objects properties, including those, used in other fs.* rulesets.
So it's only a matter of taste which one to choose.

Order
-----

Searching for rule in ruleset continues until first match is found
according to priorities.

Default rules priorities:
   1. By owner
   #. By permission
   #. By regular expression
   #. By file-type
   #. Combined

So if we have following rulesets defined::

   fs.perm { +0100 = DARK_RED }
   fs.type { file = WHITE }
   fs.owner { root = DARK_BLUE }

And if there is an executable file owned by root, it will be displayed using
DARK_BLUE, as owner ruleset has higher priority.

Priorities can be customized. This can be done using priority ruleset::

   fs.priority {
      type = 1
      combined = 2
      perm = 3
      regexp = 4
      owner = 5
   }

User interface (UI) widgets
---------------------------

Almost all aspects of UI look-n-feel can be customized using ``ui.*`` skin
rulesets.

Every widget defines a member called ``resolution`` which contains
a sequence of ruleset names in decreasing priority.
So, for instance, a MessageBox widget defines a member::

   resolution = ("message_box", "box", "widget")

According to this definition, skin manager will first look for ``message_box``
ruleset, next for ``box`` and at last for ``widget`` ruleset.
Searching stops when first of defined rulesets is found.
Default palette returned unless defined ruleset found.

A ruleset contains resources required by widget.
For detailed list of all required resources for every widget, see
the API documentation.
For example the MessageBox widget requires three resources to be defined:

- title
- mount
- box

So ruleset may look like following::

   ui.message_box {
      mount = YELLOW, DARK_GREEN
      box =  WHITE, DARK_RED
      title = YELLOW, DARK_BLUE
   }

In case such a ruleset exists in skin file, skin manager will load above
definitions and will use it for every message_box widget.
Otherwise skin manager will look for next ruleset defined in ``resolution``,
in our case it is ``box``. And so forth.

Here the following question may arise: what if some of the rulesets will not
have defined all the resources required?
The answer is simple: all missing resources take a DEFAULT color value.
