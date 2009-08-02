#!/bin/sh
./gendoc.sh && \
mkdir doc/user-manual && \
mv doc/user/.build/html/* doc/user-manual && \
 ./setup.py sdist --formats=bztar