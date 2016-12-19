#!/bin/bash

MINID="mini-dinstall --config=mini-dinstall.conf"
$MINID -k
$MINID -k
$MINID -k
rm -rf ~/debian_archive/quodlibet*
$MINID
./quodlibet.py -ddebian
./quodlibet.py -ddebian --py3
./mutagen.py -ddebian
$MINID -r
cd ~/debian_archive/quodlibet-unstable/
gpg -u B6264964! --output Release.gpg -ba Release
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
python ../build_index.py .
git add .
git commit -m "update"
git remote add origin https://github.com/lazka/ql-debian.git
git push --force --set-upstream origin gh-pages
cd -
rm -Rf ql-debian
