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
gpg -u B6264964! --output Release.gpg -ba Release
cd -

git clone https://github.com/lazka/ql-debian.git ql-debian
cd ql-debian
git checkout gh-pages
rm -rf ".git"
git init
git checkout -b gh-pages
touch  .nojekyll
rm -Rf stable
mkdir stable
cp -R ~/debian_archive/quodlibet-stable ./stable/quodlibet-stable
git add .
git commit -m "update"
git remote add origin https://github.com/lazka/ql-debian.git
git push --force --set-upstream origin gh-pages
cd -
rm -Rf ql-debian
