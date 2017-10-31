#!/bin/bash

set -e

MINID="mini-dinstall --config=mini-dinstall.conf"
$MINID -k >/dev/null 2>&1 || true
$MINID -k >/dev/null 2>&1 || true
$MINID -k >/dev/null 2>&1 || true
rm -rf ~/debian_archive
$MINID
./quodlibet.py -ddebian
./mutagen.py -ddebian
$MINID -r
cd ~/debian_archive/quodlibet-unstable/
gpg -u B6264964! --output Release.gpg -ba Release
cd -

rm -Rf ql-debian
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
python ../build_index.py .
git add .
git commit -m "update"
git remote add origin https://github.com/lazka/ql-debian.git
git push --force --set-upstream origin gh-pages
cd -
rm -Rf ql-debian
rm -rf ~/debian_archive
