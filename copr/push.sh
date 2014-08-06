#!/bin/sh

# create a srpm
mkdir workingdir
cd workingdir
mkdir SOURCES
cd SOURCES
wget `rpmspec -P ../../quodlibet.spec | grep Source0 | cut -f9 -d' '`
cd ..
cd ..
echo `pwd`
rpmbuild --define "_topdir ./workingdir" -bs quodlibet.spec

# create a git repo, push to github
cd workingdir
git init
git add .
git commit -m "update"
git remote add origin https://github.com/lazka/ql-copr.git
git push --force
cd ..

# tell copr to build it
srpm_path=$(find -name "*src.rpm")
bname=$(basename $srpm_path)

./new_build.py "https://github.com/lazka/ql-copr/raw/master/SRPMS/$bname"

# clean up
rm -Rf workingdir
