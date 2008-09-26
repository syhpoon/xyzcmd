=========
Key-codes
=========

|XYZ| has an ability to bind different keystrokes (shortcuts) to some actions,
usually to methods, exported by various plugins. In order to properly work on
any pseudo-terminal, there should be some kind of mapping different keycodes
to a predefined set of phisical keys on a keyboard.
And that's the termcap/terminfo database is for. It describes various
terminal capabilities.

Unfortunately, the urwid library, which is the console visual library 
used by |XYZ|, does not use the terminfo database for keycodes processing.
Instead it uses a set of hardcoded values found in most popular
pseudo-terminals.
However it is quite possible that your terminal codes aren't supported
(actually my cons25r FreeBSD terminal has no corresponding code entries
in urwid internal codes handler).

But fear not, |XYZ| has its own codes handler wrapper. It is accessible in
``:core:keycodes`` plugin methods.
:func:`learn_keys` method invokes an interactive dialog and user is prompted
to press a bunch of keys.

Using keycodes data file, it is possible to completely
redefine keys. For instance if one had F10 key remapped to physical TAB key,
then pressing TAB would cause the application to believe that F10 key
was pressed.

Learned data is stored in :file:`~/.xyzcmd/data/keycodes` file.

.. note::

   Please note, that data is stored in subsections based on TERM environment
   variable value. Thus all keycodes, which were learned by invoking 
   ``learn_keys`` in xterm will be saved in ``xterm``
   subsection and won't conflict with ones learned in ``cons25`` etc.

So in case you need to receive user input, :func:`xyz.input.get` method should
be used, which will honour learned keycodes data, and not
:func:`xyz.screen.get_input`.
