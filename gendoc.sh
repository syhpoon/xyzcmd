#!/bin/sh

# Generate xyzcmd documentation

API_OUT_DIR=doc/api

# 1. API Documentation

epydoc -o ${API_OUT_DIR} --html --name XYZCommander \
    --url 'http://xyzcmd.syhpoon.name/' \
    --exclude='libxyz.ui.lowui' --exclude-parse=lowui \
    --exclude=lowui --parse-only \
    libxyz plugins

# 2. User manual

cd doc/user && make clean && make html