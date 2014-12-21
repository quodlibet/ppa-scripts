#!/bin/bash

MINID="mini-dinstall --config=mini-dinstall.conf"
$MINID -k
$MINID -k
$MINID -k
rm -rf ~/debian_archive/quodlibet*
$MINID
./quodlibet.py -ddebian
./mutagen.py -ddebian
$MINID -r
cd ~/debian_archive/quodlibet-unstable/
gpg --output Release.gpg -ba Release
cd -

git clone https://github.com/lazka/ql-debian.git ql-debian
cd ql-debian
git checkout gh-pages
rm -rf ".git"
git init
git checkout -b gh-pages
touch  .nojekyll
rm -Rf testing
mkdir testing
cp -R ~/debian_archive/quodlibet-unstable ./testing/quodlibet-unstable
git add .
git commit -m "update"
git remote add origin https://github.com/lazka/ql-debian.git
git push --force
cd -
rm -Rf ql-debian
