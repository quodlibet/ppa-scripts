#!/bin/sh
mini-dinstall -k
mini-dinstall -k
mini-dinstall -k
rm -rf ~/debian_archive/quodlibet*
mini-dinstall
./quodlibet.py -ddebian
./mutagen.py -ddebian
mini-dinstall -r
cd ~/debian_archive/quodlibet-unstable/
gpg --output Release.gpg -ba Release
cd -

cd ~/debian_archive || exit
rm -rf .?*
git init
git checkout -b gh-pages
touch  .nojekyll
git add quodlibet-unstable
git add .nojekyll
git commit -m "update"
git remote add origin https://github.com/lazka/ql-debian.git
git push --force
cd -
