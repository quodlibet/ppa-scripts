#!/bin/sh
./rpm.py
./copr/push.sh
./quodlibet.py
./quodlibet.py --py3
./mutagen.py
./build-debian.sh
