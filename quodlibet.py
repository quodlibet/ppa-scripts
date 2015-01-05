#!/usr/bin/env python

import os
from _util import *

##########################################################

PACKAGE= "quodlibet"
RELEASE_TAG = "quodlibet-3.3.0"
PPA_VERSION = "3.3.99"
RELEASE_VERSION = "3.3.0"

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
clean(start_dir, PACKAGE, "exfalso")

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
    UPSTREAM_VERSION = PPA_VERSION + "+" + rev_num + "~" + rev_hash
else:
    UPSTREAM_VERSION = RELEASE_VERSION
if args.version != 0:
    UPSTREAM_VERSION += "+%s" % args.version
p("tar -pczf %s_%s.orig.tar.gz %s" % (PACKAGE, UPSTREAM_VERSION, PACKAGE))

cd(PACKAGE)

if args.dist == "debian":
    if args.release:
        releases = {"quodlibet-stable": "debian_quodlibet"}
    else:
        releases = {"quodlibet-unstable": "debian_quodlibet"}
else:
    releases = {
        "precise": "debian_quodlibet",
        "trusty": "debian_quodlibet",
        "utopic": "debian_quodlibet",
        "vivid": "debian_quodlibet",
    }

for release, debian_dir in releases.iteritems():
    p("rm -R debian")
    p("cp -R ../../%s ." % debian_dir)
    p("mv %s debian" % debian_dir)

    debian_version = "%s-0~ppa%s~%s" % (UPSTREAM_VERSION, args.version, release.replace("-", "~"))

    changelog = "debian/changelog"
    t = open(changelog).read()
    t = t.replace("%version%", debian_version)
    t = t.replace("%dist%", release)
    t = t.replace("%date%", date)
    with open(changelog, "w") as h:
        h.write(t)

    if args.dist == "debian":
        if args.release:
            fail(p("pdebuild --use-pdebuild-internal --debbuildopts '-uc -us' --buildresult .."))
        else:
            fail(p("dpkg-buildpackage -uc -us -tc -I -rfakeroot"))
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
    # fail(p("%s experimental %s*.changes" % (dput, PACKAGE)))

clean(start_dir, PACKAGE, "exfalso")
