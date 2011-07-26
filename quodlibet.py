#!/usr/bin/env python
import subprocess
import os
import sys

release_flag = False
release_rev = "quodlibet-2.3.1"
release_ver = "2.3.1"
release_ver += "-0"

#########################################################
###################### Settings #########################
#########################################################
package = "quodlibet"
package_version = "2.3.1.99-0"
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
    return p.returncode, stdout.strip(), stderr.strip()

def clean():
    global start, package
    os.chdir(start)
    cmd = "rm %s*.changes %s*.tar.gz %s*.dsc %s*.upload  %s*.build" % ((package,) * 5)
    p(cmd)

def fail(out):
    status, stdout, stderr = out
    if status != 0:
        print "#" * 24
        print stdout
        print stderr
        print "#" * 24
        clean()
        sys.exit()
    return out

#########################################################
# Start
#########################################################
dput_cfg = os.path.join(os.getcwd(), "dput.cf")

releases = {
    "lucid": "debian_quodlibet",
    "maverick": "debian_quodlibet",
    "natty": "debian_quodlibet",
    "oneiric": "debian_quodlibet",}

hg_dir = "quodlibet-hg"
if not os.path.isdir(hg_dir):
    p("hg clone https://quodlibet.googlecode.com/hg/ %s" % hg_dir)
os.chdir(hg_dir)

start = os.getcwd()
clean()

p("hg revert --all")
p("hg pull")
p("hg up default -C")
if release_flag:
    p("hg up -r%s" % release_rev)

rev = p("hg tip")[1].split()[1].replace(":","~")
date = p("date -R")[1]

os.chdir(package)

debian = "debian_quodlibet"
for release in "lucid maverick natty oneiric".split():
    p("rm -R debian")
    p("cp -R ../../%s ." % debian)
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

    fail(p("debuild -uc -us -S -I -rfakeroot"))

p("rm -R debian")
os.chdir("..")
fail(p("debsign %s*.changes %s*.dsc" % ((package,) * 2)))

dput = "dput --config '%s'" % dput_cfg
if release_flag:
    fail(p("%s stable %s*.changes" % (dput, package)))
else:
    fail(p("%s unstable %s*.changes" % (dput, package)))
#fail(p("%s experimental %s*.changes" % (dput, package)))

clean()
