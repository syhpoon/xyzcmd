#!/bin/sh

find . -name \*.pyc -delete
rm -f MANIFEST
rm -rf dist
rm -rf build
rm -f doc/api/*

cd doc/user && make clean
