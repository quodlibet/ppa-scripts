#!/usr/bin/env python

import os
from _util import *

##########################################################

PACKAGE= "quodlibet-plugins"
RELEASE_TAG = "quodlibet-2.4.0"
PPA_VERSION = "1:2.4.0.99-0"
RELEASE_VERSION = "1:2.4-0"

##########################################################

args = parse_args()

if args.dist == "ubuntu":
    dput_cfg = os.path.join(os.getcwd(), "dput.cf")
else:
    dput_cfg = os.path.join(os.getcwd(), "dput_debian.cf")

hg_dir = "quodlibet-hg"
if not os.path.isdir(hg_dir):
    p("hg clone https://quodlibet.googlecode.com/hg/ %s" % hg_dir)
cd(hg_dir)

start_dir = os.getcwd()
clean(start_dir, PACKAGE)

try: os.rename(PACKAGE, "plugins")
except OSError: pass

p("hg revert --all")
p("hg pull")
p("hg up default -C")
if args.release:
    p("hg up -r%s" % RELEASE_TAG)

rev = p("hg tip")[1].split()[1].replace(":","~")
date = p("date -R")[1]

os.rename("plugins", PACKAGE)

cd(PACKAGE)

if args.dist == "debian":
    releases = ["quodlibet-unstable"]
else:
    releases = ["lucid", "maverick", "natty", "oneiric"]

debian_dir = "debian_quodlibet-plugins"
for release in releases:
    p("rm -R debian")
    p("cp -R ../../%s ." % debian_dir)
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
os.rename(PACKAGE, "plugins")
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
