#!/usr/bin/env python3

import os
from _util import *

##########################################################

PACKAGE= "quodlibet"
RELEASE_VERSION = "4.6.0"

##########################################################

args = parse_args()

if args.dist == "ubuntu":
    dput_cfg = os.path.join(os.getcwd(), "dput.cf")
else:
    dput_cfg = os.path.join(os.getcwd(), "dput_debian.cf")

start_dir = os.getcwd()
clean(start_dir, PACKAGE, "exfalso")

git_dir = "quodlibet-git"
if not os.path.isdir(git_dir):
    p("git clone https://github.com/quodlibet/quodlibet.git %s" % git_dir)
cd(git_dir)

p("git reset HEAD --hard")
p("git clean -xfd")
p("git checkout main")
p("git pull --all")
fail(p("git checkout release-%s" % RELEASE_VERSION))

rev_num = p("git rev-list --count HEAD")[1]
rev_hash = p("git rev-parse --short HEAD")[1]
rev = rev_num  +"~" + rev_hash
date = p("date -R")[1]

UPSTREAM_VERSION = RELEASE_VERSION
if args.version != 0:
    UPSTREAM_VERSION += "+%s" % args.version

p("git archive --prefix=quodlibet/ --format=tar.gz HEAD -o ../%s_%s.orig.tar.gz" % (PACKAGE, UPSTREAM_VERSION))

debian_dir = "debian_quodlibet"

if args.dist == "debian":
    releases = {"quodlibet-stable": debian_dir}
else:
    releases = {
        "focal": debian_dir,
        "jammy": debian_dir,
        "lunar": debian_dir,
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
        fail(p("pdebuild --use-pdebuild-internal --debbuildopts '-uc -us' --buildresult .."))
    else:
        fail(p("dpkg-buildpackage -uc -us -S -tc -I -rfakeroot"))

p("rm -R debian")
cd("..")

while 1:
    out = p("debsign -k '0EBF 782C 5D53 F7E5 FB02  A667 46BD 761F 7A49 B0EC' %s*.changes" % (PACKAGE,))
    if not failed(out):
        break
    else:
        print(out)

dput = "dput --config '%s'" % dput_cfg
if args.dist == "debian":
    fail(p("%s local %s*.changes" % (dput, PACKAGE)))
else:
    fail(p("%s stable %s*.changes" % (dput, PACKAGE)))

clean(start_dir, PACKAGE, "exfalso")
