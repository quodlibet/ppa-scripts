#!/bin/bash

# needs a pbuilder:
# sudo pbuilder create --distribution stable
# sudo pbuilder update

MINID="mini-dinstall --config=mini-dinstall.conf"
$MINID -k
$MINID -k
$MINID -k
rm -rf ~/debian_archive/quodlibet*
$MINID
./quodlibet.py -ddebian --release
./mutagen.py -ddebian --release
$MINID -r
cd ~/debian_archive/quodlibet-stable/
gpg --output Release.gpg -ba Release
cd -

git clone https://github.com/lazka/ql-debian-stable.git ql-debian-stable
cd ql-debian-stable
git checkout gh-pages
rm -rf ".git"
git init
git checkout -b gh-pages
touch  .nojekyll
rm -Rf quodlibet-stable
cp -R ~/debian_archive/quodlibet-stable .
git add .
git commit -m "update"
git remote add origin https://github.com/lazka/ql-debian-stable.git
git push --force
cd -
rm -Rf ql-debian
