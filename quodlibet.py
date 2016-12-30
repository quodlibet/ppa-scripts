#!/usr/bin/env python

import os
from _util import *

##########################################################

PACKAGE= "quodlibet"
PPA_VERSION = "3.8.99"
RELEASE_VERSION = "3.8.0"

##########################################################

args = parse_args()
if args.py3:
    PACKAGE += "-py3"

if args.dist == "ubuntu":
    dput_cfg = os.path.join(os.getcwd(), "dput.cf")
else:
    dput_cfg = os.path.join(os.getcwd(), "dput_debian.cf")

git_dir = "quodlibet-git"
if not os.path.isdir(git_dir):
    p("git clone https://github.com/quodlibet/quodlibet.git %s" % git_dir)
cd(git_dir)

start_dir = os.getcwd()
clean(start_dir, PACKAGE, "exfalso")

p("git reset HEAD --hard")
p("git clean -xfd")
p("git checkout master")
p("git pull --all")
if args.release:
    fail(p("git checkout release-%s" % RELEASE_VERSION))

rev_num = p("git rev-list --count HEAD")[1]
rev_hash = p("git rev-parse --short HEAD")[1]
rev = rev_num  +"~" + rev_hash
date = p("date -R")[1]

if not args.release:
    p("echo 'BUILD_INFO = u\"%s\"' >> 'quodlibet/quodlibet/build.py'" % rev_hash)

if not args.release:
    UPSTREAM_VERSION = PPA_VERSION + "+" + rev_num + "~" + rev_hash
else:
    UPSTREAM_VERSION = RELEASE_VERSION
if args.version != 0:
    UPSTREAM_VERSION += "+%s" % args.version
p("tar -pczf %s_%s.orig.tar.gz %s" % (PACKAGE, UPSTREAM_VERSION, "quodlibet"))

cd("quodlibet")

if args.release:
    assert not args.py3
    debian_dir = "debian_quodlibet_stable"
else:
    if args.py3:
        debian_dir = "debian_quodlibet_py3"
    else:
        debian_dir = "debian_quodlibet"

if args.dist == "debian":
    if args.release:
        releases = {"quodlibet-stable": debian_dir}
    else:
        releases = {"quodlibet-unstable": debian_dir}
else:
    releases = {
        "trusty": debian_dir,
        "xenial": debian_dir,
        "yakkety": debian_dir,
        "zesty": debian_dir,
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
fail(p("debsign -k B6264964 %s*.changes %s*.dsc" % ((PACKAGE,) * 2)))

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
