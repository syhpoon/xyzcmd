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

Filesystem objects
------------------
File objects can be highlighted using FSRule descriptions.
See :ref:`FSRule` for detailed information about syntax.

File object rules are defined in **fs.rules** section of rules
argument of :func:`skin` function.

General fs ruleset definition syntax::

   "fs.rules": [
      (fsrule('<FSRule string>'),
      <Palette config>),
      ...
   ]

Here, `<FSRule string>` is a FSRule string describing filesystem object.

`<Palette config>` is a definition of object visual representation.
See :ref:`palette` for :func:`palette` description.

Colors
------
Available foreground colors:

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

Available background colors:

      * BLACK
      * BROWN
      * DEFAULT
      * DARK_RED
      * DARK_GREEN
      * DARK_BLUE
      * DARK_MAGENTA
      * DARK_CYAN
      * DARK_GRAY
      * LIGHT_GRAY

Available foreground attributes:

      * BOLD
      * UNDERLINE
      * BLINK
      * DEFAULT

Attributtes can be set in a list, including more than one value at a time.

With urwid library version starting from 0.9.9 it is possible to provide
additional colors, if terminal emulator supports this feature.

Also note, that high-colors mode is only available for raw display driver 
(term_lib in main.xyz or -d switch).

Extended colors can be specified in following formats::

 * '#009' (0% red, 0% green, 60% red, like HTML colors)
 * '#fcc' (100% red, 80% green, 80% blue)
 * 'g40' (40% gray, decimal), 'g#cc' (80% gray, hex),
 * '#000', 'g0', 'g#00' (black),
 * '#fff', 'g100', 'g#ff' (white)
 * 'h8' (color number 8), 'h255' (color number 255)

So, regular files with executable bits set can be matched as following::

   "fs.rules": [(
      fsrule(r"type{file} and perm{+0111}"),
      palette({
         "foreground": "WHITE",
         "background": "BLACK"})
   )]

Additional rule::

   "fs.rules": [(
      fsrule(r"""type{dir} or type{file} and (owner{user} or owner{root})
                 and perm{+4000}"""),
      palette({
         "foreground": "DARK_RED",
         "background": "BLACK"
       })
     )]

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

   "ui.message_box": [(
      "mount": palette({
          "foreground": "YELLOW",
          "background": "DARK_GREEN"
          })),

      ("box": palette({
          "foreground": "WHITE",
          "background": "DARK_RED"
          })),
      ("title": palette({
          "foreground": "YELLOW",
          "background": "DARK_BLUE"
          }))
   ]

In case such a ruleset exists in skin file, skin manager will load above
definitions and will use it for every message_box widget.
Otherwise skin manager will look for next ruleset defined in ``resolution``,
in our case it is ``box``. And so forth.
