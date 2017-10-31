#!/bin/sh
./rpm.py
./copr/push.sh
./quodlibet.py
./mutagen.py
./build-debian.sh
