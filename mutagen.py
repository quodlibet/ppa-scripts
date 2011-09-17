#!/usr/bin/env python

import os
from _util import *

##########################################################

PACKAGE= "mutagen"
RELEASE_TAG = "mutagen-1.20"
PPA_VERSION = "1.20.0.99-0"
RELEASE_VERSION = "1.20-0"

##########################################################

args = parse_args()

if args.dist == "ubuntu":
    dput_cfg = os.path.join(os.getcwd(), "dput.cf")
else:
    dput_cfg = os.path.join(os.getcwd(), "dput_debian.cf")

debian_root = os.getcwd()

svn_dir = "mutagen-svn"
if not os.path.isdir(svn_dir):
    os.mkdir(svn_dir)

os.chdir(svn_dir)

if not os.path.isdir(PACKAGE):
    fail(p("svn checkout http://mutagen.googlecode.com/svn/ %s" % PACKAGE))

os.chdir(PACKAGE)
p("svn revert -R .")
rev = fail(p("svn up"))[1].split()[-1].strip()[:-1]
date = p("date -R")[1]

if args.release:
    os.chdir("tags")

start_dir = os.getcwd()
clean(start_dir, PACKAGE)

if args.release:
    os.chdir(RELEASE_TAG)
else:
    os.chdir("trunk")

if args.dist == "debian":
    releases = ["unstable"]
else:
    releases = ["lucid", "maverick", "natty", "oneiric"]

debian_dir = "debian_mutagen"
for release in releases:
    p("rm -R debian")
    p("cp -R %s/%s ." % (debian_root, debian_dir))
    p("mv %s debian" % debian_dir)

    if not args.release:
        version_str = "%s~rev%s~ppa%s" % (PPA_VERSION, rev, args.version)
    else:
        version_str = "%s~ppa%s" % (RELEASE_VERSION, args.version)

    changelog = "debian/changelog"
    t = open(changelog).read()
    t = t.replace("%version%", version_str)
    t = t.replace("%dist%", release)
    t = t.replace("%date%", date)
    open(changelog, "w").write(t)

    if args.dist == "debian":
        fail(p("dpkg-buildpackage -tc -uc -us -I -rfakeroot"))
    else:
        fail(p("dpkg-buildpackage -uc -us -S -I -rfakeroot"))

p("rm -R debian")
cd("..")
fail(p("debsign %s*.changes %s*.dsc" % ((PACKAGE,) * 2)))

dput = "dput --config '%s'" % dput_cfg
if args.dist == "debian":
    fail(p("%s local %s*.changes" % (dput, PACKAGE)))
else:
    if args.release:
        fail(p("%s stable %s*.changes" % (dput, PACKAGE)))
    else:
        fail(p("%s unstable %s*.changes" % (dput, PACKAGE)))
    #fail(p("%s experimental %s*.changes" % (dput, PACKAGE)))

clean(start_dir, PACKAGE)
