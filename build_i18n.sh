#!/bin/sh

find . -name \*.py -or -name \*.xyz | xargs pygettext -o ./locale/xyzcmd.pot

chdir ./locale

for po in `find . -maxdepth 1 -type d | egrep -v "^\.$"`; do
    b=$(basename $po)

    msgfmt.py -o $b/LC_MESSAGES/xyzcmd.mo \
	./$b/LC_MESSAGES/xyzcmd.po;
done
