#!/bin/sh
./gendoc.sh && \
./build_i18n.sh && \
mkdir doc/user-manual && \
mv doc/user/.build/html/* doc/user-manual && \
./setup.py sdist --formats=bztar
