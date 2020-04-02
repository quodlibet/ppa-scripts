#!/usr/bin/env python

import os
from _util import *

##########################################################

PACKAGE = "python2-mutagen"
PPA_VERSION = "1.43.9999"
RELEASE_VERSION = "1.43.0"

##########################################################

args = parse_args()

if args.dist == "ubuntu":
    dput_cfg = os.path.join(os.getcwd(), "dput.cf")
else:
    dput_cfg = os.path.join(os.getcwd(), "dput_debian.cf")

start_dir = os.getcwd()
clean(start_dir, PACKAGE, "python-" + PACKAGE, "python3-" + PACKAGE)

git_dir = "mutagen-git"
if not os.path.isdir(git_dir):
    p("git clone https://github.com/quodlibet/mutagen.git %s" % git_dir)
cd(git_dir)

p("git reset HEAD --hard")
p("git clean -xfd")
p("git checkout master")
p("git pull --all")
if args.release:
    fail(p("git checkout release-%s" % RELEASE_VERSION))
else:
    fail(p("git checkout release-%s" % RELEASE_VERSION))

rev_num = p("git rev-list --count HEAD")[1]
rev_hash = p("git rev-parse --short HEAD")[1]
rev = rev_num  +"~" + rev_hash
date = p("date -R")[1]

if not args.release:
    UPSTREAM_VERSION = PPA_VERSION + "+" + rev_num + "~" + rev_hash
else:
    UPSTREAM_VERSION = RELEASE_VERSION
if args.version != 0:
    UPSTREAM_VERSION += "+%s" % args.version

p("git archive --prefix=mutagen/ --format=tar.gz HEAD -o ../%s_%s.orig.tar.gz" % (PACKAGE, UPSTREAM_VERSION))

if args.dist == "debian":
    if args.release:
        releases = {"quodlibet-stable": "debian_mutagen_py2"}
    else:
        releases = {"quodlibet-unstable": "debian_mutagen_py2"}
else:
    releases = {
        "xenial": "debian_mutagen_py2",
        "bionic": "debian_mutagen_py2",
        "eoan": "debian_mutagen_py2",
    }

for release, debian_dir in releases.items():
    p("rm -R debian")
    p("cp -R ../%s ." % debian_dir)
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

while 1:
    out = p("debsign -k '0EBF 782C 5D53 F7E5 FB02  A667 46BD 761F 7A49 B0EC' %s*.changes" % (PACKAGE,))
    if not failed(out):
        break

dput = "dput --config '%s'" % dput_cfg
if args.dist == "debian":
    fail(p("%s local %s*.changes" % (dput, PACKAGE)))
else:
    if args.release:
        fail(p("%s stable %s*.changes" % (dput, PACKAGE)))
    else:
        fail(p("%s unstable %s*.changes" % (dput, PACKAGE)))
    # fail(p("%s experimental %s*.changes" % (dput, PACKAGE)))

clean(start_dir, PACKAGE, "python-" + PACKAGE, "python3-" + PACKAGE)
