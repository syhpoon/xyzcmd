=======
FSRules
=======

FSRules - это широко используемый в |XYZ| мини-DSL для создания правил
описания объектов файловой системы.

Каждое правило это предикат - то есть передавая ему аргументом объект
VFS мы получаем значение :const:`True` либо :const:`False` в зависимости
от того, совпадает ли параметры, указанные в правиле с параметрами
данного конкретного объекта.

Грамматика правил ``FSRules`` (БНФ)

.. productionlist::
    rule          : expr $
                  : expr op rule
    expr          : expr_body
                  : NOT expr_body
                  : "(" rule ")"
    expr_body     : ftype "{" ARG "}"
    op            : "and" | "or"
    ftype         : "type" | "perm" | "owner" | "regexp"
                  : "link_type" | "link_perm" | "link_owner"
                  : "link_regexp" | "link_exists"

Каждое правило состоит из одного или более выражений объединённых логическими
операторами.

Как видно из грамматики, выражение имеет вид ``<type>{<arg>}``.
Доступные типы выражений:

* :ref:`type`
* :ref:`perm`
* :ref:`owner`
* :ref:`regexp`
* :ref:`link_type <type>`
* :ref:`link_perm <perm>`
* :ref:`link_owner <owner>`
* :ref:`link_regexp <regexp>`
* :ref:`link_exists`

``link_type, link_perm, link_owner, link_regexp`` are the same expressions
as corresponding above, but they're applied only for symbolic links targets.

Логический смысл выражения можно изменить на противоположный добавив оператор
``not`` перед ним.

Expressions in a rule are combined using logical operators 
:ref:`and <logical_op>` and :ref:`or <logical_op>`.

.. _type:

type
----

Выражение ``type`` используется для определения типа файлового объекта.
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

Выражение ``perm`` определяет биты доступа файлового объекта.
Аргумент задаётся в формате: ``[+]dddd``.

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

.. _link_exists:

link_exists
-----------
``link_exists`` expression is used to indicate whether a symbolic link target
(i.e. the object the link refers to) exists.

Actually ``link_exists`` expression does not need any arguments, but
as ``FSRules`` parser requires the expressions to have exactly one
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
