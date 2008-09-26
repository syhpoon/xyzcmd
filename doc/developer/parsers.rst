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
* Quoted string can be one-line: ``"quoted value"``,
  or multiline::

   '''
   quoted value1,
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
   *Default: \\n*

**validvars**
   A list of valid variable names.
   *Default: ()*

**value_validator**
   A function that takes three args: current block, var and value
   and validates them. In case value is invalid, :exc:`XYZValueError` 
   must be raised. Otherwise function must return required value,
   possibly modified.
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

Here result is a :class:`libxyz.parser.ParsedData` instance contained
all parsed data from conf file.

FlatParser
----------
FlatParser is simple linear parser, it is used to parse single-line expressions.
Parseable format is following:
``var1 <assign> val1[<list_separator>,...] <delimiter>``.

FlatParser takes following options (all the options have the same meaning as
the ones of BlockParser):

* comment
* assignchar
* delimiter
* validvars
* value_validator
* list_separator

RegexpParser
------------
As name implies, RegexpParser is used to parse files using regular expressions.

RegexpParser constructor takes a single argument: a dictionary, where keys
are compiled regular expressions (using :func:`re.compile`), and
values are callback-functions.

Upon matching, RegexpParser will call appropriate callback with
:class:`MatchObject` as argument.

Callback-function must raise :exc:`libxyz.exceptions.XYZValueError` in case
of any error, or return anything otherwise.

.. note::
   RegexpParser is a line-based parser. Thus it is not suitable for parsing
   any non-linear multiline structures. Use BlockParser instead.

If RegexpParser is unable to match a line within any of provided parsers,
it will raise :exc:`libxyz.exceptions.ParseError`

Example
+++++++
A RegexpParser common usage example::

   import re
   from libxyz.parsers import RegexpParser

   symtable = {}

   # Assign expression callback, put variable and value to internal symtable
   def cb_assign(mo):
      global symtable

      var = mo.group("variable")
      val = mo.group("value")

      symtable[var] = val

   re_comment = re.compile(r"^\s*#.*$")
   re_assign = re.compile(r"^\s*(?<variable>\w+)\s*=\s*(?<value>\w+)\s*$")

   cbpool = {re_comment: lambda: None, re_assign: cb_assign}

   parser = RegexpParser(cbpool)
   parser.parse("# Comment\n x = y")

MultiParser
-----------
So far we've seen all the available parsers in libxyz.
But all of those parsers designed to parse single source from the beginning to
the end. Quite often it is exactly what you want. But sometimes, you'd want
to mix several different syntices in a single source. That's exactly
the MultiParser is for. It's actually a wrapper around another parser types.

MultiParser can take following options:

**comment**
   A commentary character.
   *Default: #*

**tokens**
   A sequence of tokens.
   *Default: ()*

As its first argument, MultiParser constructor takes a dictionary, where
keys could be either string, or sequence or compiled regexp and values
are any valid parser instance.

So MultiParser acts as follows:

* Get a token from lexer
* Try to match a token against any key in parsers dictionary
* If matched, call appropriate parser instance :func:`parse` method
* If not found, try to match a token against all the sequences in parsers dict
* If not found try to match a token against all regular expressions in parser dict

.. note::
   Usually all the parsers provided to MultiParser, have option **count** set 
   to 1. Because parsing single expression does not mean that, the following
   expression in source would be the same type and would require the
   same parser to use.

And that's it.
Let's assume we want to parse a configuration file with following syntax::

   # Comment
   VAR1: VAL1 # Flat expression

   # Block expression
   block {
      var = val
   }

Now let's take a look at how we would manage to parse such a file::

   import libxyz.parser
   import re

   # Parser options
   flat_opts = {u"count": 1, u"assingchar": u":"}
   block_opts = {u"count": 1}

   flat_p = libxyz.parser.FlatParser(flat_opts)
   block_p = libxyz.parser.BlockParser(block_opts)
   multi_p = libxyz.parser.MultiParser({})
   multi_p.register(re.compile(r"VAR\d+"), flat_p)
   multi_p.register(u"block", block_p)

   data = multi_p.parse(file("config.file"))
