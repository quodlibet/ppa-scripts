#!/usr/bin/env python
import subprocess
import os
import sys

release_flag = False
release_tag = "mutagen-1.20"
release_ver = "1.20"
release_ver += "-0"

#########################################################
###################### Settings #########################
#########################################################
package = "mutagen"
package_version = "1.20.0.99-0"
ppa_version = "2"
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

debian_root = os.getcwd()

svn_dir = "mutagen-svn"
if not os.path.isdir(svn_dir):
    os.mkdir(svn_dir)

os.chdir(svn_dir)

if not os.path.isdir(package):
    fail(p("svn checkout http://mutagen.googlecode.com/svn/ %s" % package))

os.chdir(package)
p("svn revert -R .")
rev = fail(p("svn up"))[-1].split()[-1].strip()[:-1]
date = p("date -R")[-1]

if release_flag:
    os.chdir("tags")
start = os.getcwd()
clean()
if release_flag:
    os.chdir(release_tag)
else:
    os.chdir("trunk")

debian = "debian_mutagen"
for release in "lucid karmic jaunty hardy maverick".split():
    p("rm -R debian")
    p("cp -R %s/%s ." % (debian_root, debian))
    p("mv %s debian" % debian)

    if not release_flag:
        version_str = "%s~rev%s~ppa%s" % (package_version, rev, ppa_version)
    else:
        version_str = "%s~ppa%s" % (release_ver, ppa_version)

    changelog = "debian/changelog"
    t = open(changelog).read()
    t = t.replace("%version%", version_str)
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
