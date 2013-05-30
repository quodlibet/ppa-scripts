#!/bin/sh
mini-dinstall -k
mini-dinstall -k
mini-dinstall -k
rm -rf ~/debian_archive/quodlibet*
mini-dinstall
./quodlibet.py -ddebian
./quodlibet-plugins.py -ddebian
./mutagen.py -ddebian
mini-dinstall -r
cd ~/debian_archive/quodlibet-unstable/
gpg --output Release.gpg -ba Release
cd -
./debian_upload.py
