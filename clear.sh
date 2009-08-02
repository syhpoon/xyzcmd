#!/bin/sh

find . -name \*.pyc -delete
rm -f MANIFEST
rm -rf dist
rm -rf build
rm -f doc/api/*
rm -rf doc/user-manual

cd doc/user && make clean
