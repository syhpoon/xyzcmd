#!/bin/sh
export DEBFULLNAME="Max E. Kuznecov"
export DEBEMAIL="syhpoon@syhpoon.name"

./build.sh && dpkg-buildpackage -us -uc