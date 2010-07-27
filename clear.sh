#!/bin/sh

find . -name \*.pyc -delete
rm -f MANIFEST
rm -rf dist
rm -rf build
rm -f doc/api/*
rm -rf doc/user-manual
rm -rf debian/python-module-stampdir
rm -rf debian/xyzcmd
rm -f debian/xyzcmd.debhelper.log
rm -f debian/xyzcmd.postinst.debhelper
rm -f debian/xyzcmd.preinst.debhelper
rm -f debian/xyzcmd.prerm.debhelper
rm -f debian/xyzcmd.substvars
rm -f po/mo/*

cd doc/user && make clean
