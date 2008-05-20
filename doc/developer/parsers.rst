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
**TBD**

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

FlatParser
----------
**TBD**

RegexpParser
------------
**TBD**

MultiParser
-----------
**TBD**
