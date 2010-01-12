.. include:: includes.inc

=====
Skins
=====

Skins are used to configure visual representation of |XYZ|.
Customizable elements are:

* Elements of filesystem based on :ref:`FSRule` description:
* All user interface widgets

Skin-definition file is a python-script file containing skin-directives.
Skin-files may be located in skins subdirectory of xyzcmd main installation
path or in user .xyzcmd/skins directory.
All files in those directories executed
for script definitions. Although single skin file can contain multiple
skin definitions, it is advisable to put only one skin into an appropriately
 named file.

Skins are defined using :func:`skin` DSL function (see :ref:`skin`).

Filesystem types
----------------
File objects can be highlighted using FSRule descriptions.
See :ref:`FSRule` for detailed information about syntax.

File object rules are defined in **fs.rules** section of rules
dictionary argument of :func:`skin` function.

General fs ruleset definition syntax::

   "fs.rules": [
      (fsrule('<FSRule string'),
      <Palette config>),
      ...
   ]

Here, `<FSRule string>` is a FSRule string describing filesystem object.

`<Palette config>` is a definition of object visual representation.

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

So, regular files with executable bits set can be matched as following::

   fs.rules {
      "type{file} and perm{+0111}" = WHITE, BLACK
   }

More complex rules can be split along several lines using x-quoted strings::

   fs.rules {
      '''
      type{dir} or type{file}
      and (owner{user} or owner{root})
      and perm{+4000}
      ''' = DARK_RED, BLACK
      }

Order
-----

Searching for rule in ruleset continues until first match is found.
The order of rules is the same as specified in skin file.

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
