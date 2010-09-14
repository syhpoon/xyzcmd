#!/bin/sh
export DEBFULLNAME="Max E. Kuznecov"
export DEBEMAIL="syhpoon@syhpoon.name"

./build.sh && dpkg-buildpackage -uc -k4778E7C0

# For ubuntu  PPA
#./build.sh && dpkg-buildpackage -uc -S -k4778E7C0
# debsign -m4778E7C0 *.changes
