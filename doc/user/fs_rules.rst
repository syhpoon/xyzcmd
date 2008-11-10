=======
FSRules
=======

FSRules is a tiny DSL, widely-used in |XYZ| for describing filesystem
objects.

Each rule produces a predicate, that is passing a VFS object as an argument,
rule yields either :const:`True` or :const:`False` depending if
described attributes match the actual ones of passed object.

FSRules grammar (BNF)

.. productionlist::
    rule          : expr $
                  : expr op rule
    expr          : expr_body
                  : NOT expr_body
                  : "(" rule ")"
    expr_body     : ftype "{" ARG "}"
<<<<<<< /home/syhpoon/UNIX/Работа/Программирование/Языки/python/Проекты/xyzcmd/xyzcmd-trunk/doc/user/fs_rules.rst
    op            : "and" | "or"
    ftype         : "type" | "perm" | "owner" | "regexp"
                  : "link_type" | "link_perm" | "link_owner"
                  : "link_regexp" | "link_exists"
                  : "size"
=======
    op            : "and"
                  : "or"
    ftype         : "type"
                  : "perm"
                  : "owner"
                  : "regexp"
                  : "size
                  : "link_type"
                  : "link_perm"
                  : "link_owner"
                  : "link_regexp"
                  : "link_exists"
                  : "link_size"
>>>>>>> /tmp/fs_rules.rst~other.pmcEt-

Rule consists of one or more expressions combined with logical operators.
<<<<<<< /home/syhpoon/UNIX/Работа/Программирование/Языки/python/Проекты/xyzcmd/xyzcmd-trunk/doc/user/fs_rules.rst

п п╟п╨ п╡п╦п╢п╫п╬ п╦п╥ пЁя─п╟п╪п╪п╟я┌п╦п╨п╦, п╡я▀я─п╟п╤п╣п╫п╦п╣ п╦п╪п╣п╣я┌ п╡п╦п╢ ``<type>{<arg>}``.
Available expressions are:
=======
Expression has the following format: ``<type>{<arg>}``.
Available expressions are:
>>>>>>> /tmp/fs_rules.rst~other.pmcEt-

* :ref:`type`
* :ref:`perm`
* :ref:`owner`
* :ref:`regexp`
* :ref:`size`
* :ref:`link_type <type>`
* :ref:`link_perm <perm>`
* :ref:`link_owner <owner>`
* :ref:`link_regexp <regexp>`
* :ref:`link_size <size>`
* :ref:`link_exists`

``link_type, link_perm, link_owner, link_regexp,  link_size``
are the same expressions as corresponding above,
but they're applied only for symbolic links targets.

Expression can be negated by prepending operator ``not`` in front of it.

Expressions in a rule are combined using logical operators 
:ref:`and <logical_op>` and :ref:`or <logical_op>`.

.. _type:

type
----

``type`` expression is used to match object based on its type.
Available arguments:

*file*
    Regular file

*dir*
    Directory

*block*
    Block device

*char*
    Char device

*link*
    Symbolic link

*fifo*
    FIFO

*socket*
    Socket

So, to match all regular files and directories use:
``"type{file} or type{dir}"``

.. _perm:

perm
----

``perm`` expression is used to match objects by permission bits.
An argument is specified as ``[+]dddd``.
Where ``dddd`` is an octal number. If number is preceeded by '+' this will
match objects with any of mode bits set. Otherwise it will
match only files with exactly the same mode as given.

Examples::

    # This will match any set-uid object
    "perm{+4000}"

    # Objects with execution bits set
    "perm{+0111}"

    # Match only objects with exactly set mode - 755
    "perm{0755}"

.. _owner:

owner
-----

``owner`` expression is used to match file object based on its owner and/or
group.

Argument can be specified as ``[uid][:gid]``. uid and gid both can be either
symbolic or numeric::

      # Files owned by root and group wheel
      "type{file} and owner{root:wheel}

      # Directories owned by username
      "type{dir} and owner{username}"

      # Sockets owned by group operator
      "type{socket} and owner{:operator}

      # Objects owner by user with uid 1050
      "owner{1050}"

.. _regexp:

regexp
------
``regexp`` expressions rules use names of object as match criteria.

An argument is an arbitrary regular-expression string. It is better to quote
the whole argument so it would be interpreted correctly by lexer::

      # *.core files
      '''regexp{".*\\.core$"}'''

      # Hidden files
      '''regexp{"^\\.{1}[^.]"}'''

<<<<<<< /home/syhpoon/UNIX/Работа/Программирование/Языки/python/Проекты/xyzcmd/xyzcmd-trunk/doc/user/fs_rules.rst
.. _size:

size
----
``size`` expressions are used to match object based on its size.

An argument has following format::

    [><][=]<size>[BKMGT]

A

=======
.. _size:

size
----
``size`` expressions are used to match objects based on their size.

General argument format is: ``[[<>]=]<size>[BbKkMmGgTt]``.
Where the only required part is ``<size>``.
An operator can be preprended to size, one of: ``>, <, >=, <=, =``.
If operator is omitted, ``=`` is assumed.
Also a modifier can be appended::

   bB - The size in bytes (default)
   kK - The size in kilobytes
   mM - The size in megabytes
   gG - The size in gigabytes
   tG - The size in terabytes

If no modifier is used, the size is considered to be in bytes.

Some examples::

   # Files larger than 100 megabytes
   size{">=100M"}

   # Exactly 700 bytes, also can be written as size{"=700B"}
   size{700}

>>>>>>> /tmp/fs_rules.rst~other.pmcEt-
.. _link_exists:

link_exists
-----------
``link_exists`` expression is used to indicate whether a symbolic link target
(i.e. the object the link refers to) exists.

Actually ``link_exists`` expression does not need any arguments, but
because of ``FSRules`` parser requires the expressions to have exactly one
argument, a ``?`` character is usually specified::

    # Match all broken links
    "not link_exists{?}"

.. _logical_op:

Logical operators
-----------------
Expressions can be combined using logical operators ``and`` and ``or``.
Expression are calculated in a short-circuit scheme, that is second argument
is only evaluated if the first argument does not suffice to determine the
value of the expression.

Extended expressions (DEV)
--------------------------
In addition to standard built-in expressions, :class:`FSRule` parser has an 
ability to extend its functionality by adding new expression types.

Extending is done using extend() classmethod of :class:`FSRule` class, that is
new expressions are applied to class and thus are immediately
available to all :class:`FSRule` instances.

Let's say we're writing a plugin which adds a new :class:`FSRule` expression,
say: ``inode{inode}`` whose purpose is to match objects with provided inode.

So we need to prepare a transformation function and a match function.

Transformation function takes a string which was passed as an argument
and returns whatever is neccessary to match on later. In our case an argument
is an inode, so it would be enough to make sure the it is number::

   transform = lambda arg: int(arg)

Next we need a match function wich will be called when match()
method is invoked on :class:`FSRule` instance.

Match function takes two variables:
:class:`VFSFile` instance and a transformed value returned
by our transformation function above::

   match = lambda obj, arg: obj.inode is not None and obj.inode == arg

Note that match functions are required to return either :const:`True` or
:const:`False` or raise an exception in case of error.

Now we've got everything we need to extend :class:`FSRule`.
In :func:`prepare` method of our plugin we add::

   import libxyz.core.FSRule

   def prepare(self):
      transform = lambda arg: int(arg)
      match = lambda obj, arg: obj.inode is not None and obj.inode == arg

      libxyz.core.FSRule.extend("inode", transform, match) 

And in :func:`finalize` remove extended expression::

   def finalize(self):
      libxyz.core.FSRule.unextend("inode")

That's is, after |XYZ| loads our plugin, we can start using ``inode{}``
in our FSRule expressions.
