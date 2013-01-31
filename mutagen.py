#!/usr/bin/env python

import os
from _util import *

##########################################################

PACKAGE= "mutagen"
RELEASE_TAG = "mutagen-1.21"
PPA_VERSION = "1.21.99-0"
RELEASE_VERSION = "1.21-0"

##########################################################

args = parse_args()

if args.dist == "ubuntu":
    dput_cfg = os.path.join(os.getcwd(), "dput.cf")
else:
    dput_cfg = os.path.join(os.getcwd(), "dput_debian.cf")

debian_root = os.getcwd()

start_dir = os.getcwd()
clean(start_dir, PACKAGE)

hg_dir = "mutagen-hg"
if not os.path.isdir(hg_dir):
    p("hg clone https://mutagen.googlecode.com/hg/ %s" % hg_dir)
cd(hg_dir)

p("hg revert --all --no-backup")
p("hg pull")
p("hg up default -C")
if args.release:
    p("hg up -r%s" % RELEASE_TAG)

rev_num = p("hg id -n")[1]
rev_hash = p("hg id -i")[1]
rev = rev_num  +"~" + rev_hash
date = p("date -R")[1]

if args.dist == "debian":
    releases = ["quodlibet-unstable"]
else:
    releases = ["lucid", "oneiric", "precise", "quantal", "raring"]

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
        fail(p("dpkg-buildpackage -tc -uc -us -tc -I -rfakeroot"))
    else:
        fail(p("dpkg-buildpackage -uc -us -S -tc -I -rfakeroot"))

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
