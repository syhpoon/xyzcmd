#!/bin/sh

find . -name \*.py -or -name \*.xyz | xargs pygettext -o ./po/xyzcmd.pot

for po in ./po/*.po; do
    b=$(basename $po)
    msgfmt.py -o ./po/mo/${b%.po}.mo $po;
done
