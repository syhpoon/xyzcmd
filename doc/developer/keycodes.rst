=========
Key-codes
=========

|XYZ| has an ability to bind different keystrokes (shortcuts) to some actions,
usually to ones, exported by various plugins. In order to properly work on
any pseudo-terminal, there should be some kind of mapping different keycodes
to a predefined set of phisical keys on a keyboard.
And that's the termcap/terminfo database is for. It describes various
terminal capabilities.

Unfortunately, the urwid library, which is the console visual library 
used by |XYZ|, does not use the terminfo database for keycodes processing.
Instead it uses a set of hardcoded codes found in most popular pseudo-terminals.
However it is quite possible that your terminal codes aren't supported
(actually my cons25r FreeBSD terminal has no corresponding code entries
in urwid internal codes handler).

But fear not, |XYZ| has its own codes handler wrapper. It is accessible in
``:core:keycodes`` plugin methods.
``learn_keys`` method invokes an interactive dialog and user is prompted to
press a bunch of keys.

And even more, using keycodes data file, it is possible to completely
redefine keys. For instance if one has F10 key remapped to physical TAB key,
then pressing TAB would cause the application to believe that F10 key
was pressed.

Learned data is stored in *~/.xyzcmd/data/keycodes* file. Please note, that
data is stored in subsections based on TERM environment variable value.
Thus all keycodes, which was learned by invoking ``learn_keys`` in xterm will
be saved in ``xterm`` subsection and won't conflict with ones learned in
``cons25`` etc.

So in case you need to receive user input, ``xyz.input.get()`` method should
be used, which will honor learned keycodes data, and not
``xyz.screen.get_input()``.
