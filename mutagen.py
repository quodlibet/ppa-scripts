#!/usr/bin/env python
import subprocess
import os
import sys

#########################################################
###################### Settings #########################
#########################################################
package = "mutagen"
package_version = "1.18.99-0"
ppa_version = "1"
#########################################################
#########################################################

#########################################################
# Functions
#########################################################
def p(cmd):
    print "> %s" % cmd
    pipe = subprocess.PIPE
    p = subprocess.Popen(cmd, shell=True, stdout=pipe, stderr=pipe, stdin=pipe)
    stdout, stderr = p.communicate()
    return p.returncode, stdout.strip()

def clean():
    global start, package
    os.chdir(start)
    cmd = "rm %s*.changes %s*.tar.gz %s*.dsc %s*.upload" % ((package,) * 4)
    p(cmd)

def fail(out):
    status, stdout = out
    if status != 0:
        print "#" * 24
        print stdout
        print "#" * 24
        clean()
        sys.exit()
    return out

#########################################################
# Start
#########################################################
dput_cfg = os.path.join(os.getcwd(), "dput.cf")

svn_dir = "mutagen-svn"
if not os.path.isdir(svn_dir):
    os.mkdir(svn_dir)

os.chdir(svn_dir)
start = os.getcwd()
clean()

if not os.path.isdir(package):
    fail(p("svn checkout http://mutagen.googlecode.com/svn/trunk/ %s" % package))

os.chdir(package)
p("svn revert -R .")
rev = fail(p("svn up"))[-1].split()[-1].strip()[:-1]
date = p("date -R")[-1]

debian = "debian_mutagen"
for release in "lucid karmic jaunty hardy intrepid".split():
    p("rm -R debian")
    p("cp -R ../../%s ." % debian)
    p("mv %s debian" % debian)

    changelog = "debian/changelog"
    t = open(changelog).read()
    t = t.replace("%ver%", package_version)
    t = t.replace("%rev%", rev)
    t = t.replace("%ppa%", ppa_version)
    t = t.replace("%dist%", release)
    t = t.replace("%date%", date)
    open(changelog, "w").write(t)

    fail(p("dpkg-buildpackage -uc -us -S -I -rfakeroot"))

p("rm -Rf debian")
os.chdir("..")
fail(p("debsign %s*.changes %s*.dsc" % ((package,) * 2)))

dput = "dput --config %s" % dput_cfg
#fail(p("%s stable %s*.changes" % (dput, package)))
fail(p("%s unstable %s*.changes" % (dput, package)))
#fail(p("%s experimental %s*.changes" % (dput, package)))

clean()
