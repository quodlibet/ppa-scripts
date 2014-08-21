#!/usr/bin/env python

import os
from _util import *

##########################################################

PACKAGE= "mutagen"
RELEASE_TAG = "mutagen-1.24"
PPA_VERSION = "1.24.99"
RELEASE_VERSION = "1.24"

##########################################################

args = parse_args()

if args.dist == "ubuntu":
    dput_cfg = os.path.join(os.getcwd(), "dput.cf")
else:
    dput_cfg = os.path.join(os.getcwd(), "dput_debian.cf")

debian_root = os.getcwd()

start_dir = os.getcwd()
clean(start_dir, PACKAGE)
clean(start_dir, "python-" + PACKAGE)

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

if not args.release:
    VERSION = PPA_VERSION + "+" + rev_num
else:
    VERSION = RELEASE_VERSION

cd("..")

if args.dist == "debian":
    p("tar --exclude '.hg*' -pczf %s_%s-0~rev%s~ppa%s~quodlibet.orig.tar.gz %s" % (PACKAGE, VERSION, rev, args.version, hg_dir))
else:
    p("tar --exclude '.hg*' -pczf %s_%s.orig.tar.gz %s" % (PACKAGE, VERSION, hg_dir))

cd(hg_dir)

if args.dist == "debian":
    releases = ["quodlibet-unstable"]
else:
    releases = ["precise", "trusty", "utopic"]

debian_dir = "debian_mutagen"
for release in releases:
    p("rm -R debian")
    p("cp -R ../%s ." % debian_dir)
    p("mv %s debian" % debian_dir)

    if not args.release:
        version_str = "%s-0~rev%s~ppa%s" % (VERSION, rev, args.version)
    else:
        version_str = "%s-0~ppa%s" % (VERSION, args.version)

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
clean(start_dir, "python-" + PACKAGE)
