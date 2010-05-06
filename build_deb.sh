#!/bin/sh
export DEBFULLNAME="Max E. Kuznecov"
export DEBEMAIL="syhpoon@syhpoon.name"

./build.sh && dpkg-buildpackage -uc

# For ubuntu  PPA
#./build.sh && dpkg-buildpackage -uc -S -k4778E7C0
# debsign -m4778E7C0 *.changes