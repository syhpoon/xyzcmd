=======
Parsers
=======

There are several parsers available in libxyz:

   * BlockParser_
   * FlatParser_
   * RegexpParser_
   * MultiParser_

Each parser has its own usage benefits depending on data needed to parse.

General syntax
--------------
* Blank chars are usually ignored.
* Quoted string can be one-line: "quoted value",
  or multiline:'''quoted value1,
                  quoted value2,
               '''
* New-line char ends commented line if any.
* Values can be provided as simple literals or quoted ones.
* If value contains spaces or any other non-alphanumeric values it is better
  to quote it or escape it using escapechar.
* Variable can take list of values, separated by comma
* Escaping can only be used in rval position.

BlockParser
-----------
BlockParser is the the most complex parser of all available in libxyz.
It is used to parse block data. General format of parseable data is following::

   name {
      var1 <assignchar> val1 <delimiter>
      var2 <assignchar> val2 [<list_separator>val3...] <delimiter>
       ...
   }

BlockParser can take a bunch of options:

**comment**
   A commentary character. BlockParser supports only one-line commentary.
   *Default: #*

**varre**
   Compiled regular expression to be check on every variable name in block.
   *Default: r"^[\w-]+$"*

**assignchar**
   Assign char, which is placed between variable and value.
   *Default: =*

**delimiter**
   Delimiter char. It terminates single statement.
   *Default is \n*

**validvars**
   A list of valid variable names.
   *Default: ()*

**value_validator**
   A function that takes three args: current block, var and value
   and validates them. In case value is invalid, XYZValueError must be raised.
   Otherwise function must return required value, possibly modified.
   *Default: None*

**count**
   How many blocks to parse. If count <= 0 - will parse all available.
   It is usefull for MultiParser_.
   *Default: 0*

**list_separator**
   Character to separate elements in list.
   *Default: ,*

**macrochar**
   Macro character (None to disable macros).
   *Default: &*

Macros
++++++
BlockParser supports macros. Macros are special internal variables that get
expanded upon parsing. Macro definition is similar to variable definition,
but macro char (default '&') is prepended to var name::

   &macro = value
   var = &macro

Macro can hold not only a single values, but a list of values as well::

   &mlist = v1, v2, v3
   var = &mlist

Also macros can be nested::

   &m1 = value1
   &m2 = value2
   &m3 = &m1, &m2
   var = &m3

Here ``var`` will get list value ``value1, value2``.

Example
+++++++
Following example shows the simplest BlockParser usage case::

   from libxyz.parser import BlockParser

   parser = BlockParser()
   result = parser.parse(file("super.conf"))

Here result is a libxyz.parser.ParsedData instance contained all parsed data
from super.conf file.

FlatParser
----------
**TBD**

RegexpParser
------------
**TBD**

MultiParser
-----------
**TBD**
