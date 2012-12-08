#!/usr/bin/env python

import os
from _util import *

cd("quodlibet-hg")
p("hg revert --all --no-backup")
p("hg pull")
p("hg up default -C")

rev = p("hg id -n")[1]
short_hash = p("hg id -i")[1]
full_hash = p("hg parent --template '{node}'")[1]

cd("..")

if not os.path.exists("rpm"):
    os.mkdir("rpm")
cd("rpm")

if not os.path.exists("home:lazka0:ql-stable"):
    p("osc co home:lazka0:ql-stable")

if not os.path.exists("home:lazka0:ql-unstable"):
    p("osc co home:lazka0:ql-unstable")

cd("home:lazka0:ql-unstable")
cd("quodlibet")

lines = []
with open("quodlibet.spec", "rb") as f:
    for l in f:
        if l.startswith("%define hash"):
            l = "%%define hash %s\n" % short_hash
        elif l.startswith("%define longhash"):
            l = "%%define longhash %s\n" % full_hash
        elif l.startswith("%define revision"):
            l = "%%define revision %s\n" % rev
        lines.append(l)

with open("quodlibet.spec", "wb") as f:
    f.write("".join(lines))

print "diff:"
print p("osc diff")[1]
raw_input()

p("osc commit -m 'update to rev %s'" % rev)
