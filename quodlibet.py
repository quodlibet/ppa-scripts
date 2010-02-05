#!/usr/bin/env python
import subprocess
import os
import sys

release = False
release_rev = "1fcdfa4dce"
release_ver = "2.2"
release_ver += "-0"

#########################################################
###################### Settings #########################
#########################################################
package = "quodlibet"
package_version = "2.2.99-0"
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

releases = {
    "lucid": "debian_quodlibet_karmic-lucid",
    "karmic": "debian_quodlibet_karmic-lucid",
    "jaunty": "debian_quodlibet_hardy-intrepid-jaunty",
    "hardy": "debian_quodlibet_hardy-intrepid-jaunty",
    "intrepid": "debian_quodlibet_hardy-intrepid-jaunty"}

hg_dir = "quodlibet-hg"
if not os.path.isdir(hg_dir):
    p("hg clone https://quodlibet.googlecode.com/hg/ %s" % hg_dir)
os.chdir(hg_dir)

start = os.getcwd()
clean()

p("hg revert --all")
p("hg pull")
p("hg up -C")
if release:
    p("hg up -r%s" % release_rev)

rev = p("hg tip")[-1].split()[1].replace(":","~")
date = p("date -R")[-1]

os.chdir(package)
for release, folder in releases.iteritems():
    p("rm -R debian")
    p("cp -R ../../%s ." % folder)
    p("mv %s debian" % folder)

    if not release:
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

p("rm -R debian")
os.chdir("..")
fail(p("debsign %s*.changes %s*.dsc" % ((package,) * 2)))

dput = "dput --config %s" % dput_cfg
#fail(p("%s stable %s*.changes" % (dput, package)))
fail(p("%s unstable %s*.changes" % (dput, package)))
#fail(p("%s experimental %s*.changes" % (dput, package)))

clean()
