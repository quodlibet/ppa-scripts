#!/usr/bin/env python
import subprocess
import os
import sys

release_flag = False
release_rev = "213a162f6d"
release_ver = "1:2.2.1"
release_ver += "-0"

#########################################################
###################### Settings #########################
#########################################################
package = "quodlibet-plugins"
package_version = "1:2.2.99-0"
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
    global package
    status, stdout = out
    if status != 0:
        print "#" * 24
        print stdout
        print "#" * 24
        clean()
        #try renaming the folder back
        try: os.rename(package, "plugins")
        except: pass
        sys.exit()
    return out

#########################################################
# Start
#########################################################
dput_cfg = os.path.join(os.getcwd(), "dput.cf")

releases = {
    "natty": "debian_quodlibet-plugins_karmic-lucid",
    "maverick": "debian_quodlibet-plugins_karmic-lucid",
    "lucid": "debian_quodlibet-plugins_karmic-lucid",
    "karmic": "debian_quodlibet-plugins_karmic-lucid",
    "jaunty": "debian_quodlibet-plugins_hardy-intrepid-jaunty",
    "hardy": "debian_quodlibet-plugins_hardy-intrepid-jaunty"}

hg_dir = "quodlibet-hg"
if not os.path.isdir(hg_dir):
    p("hg clone https://quodlibet.googlecode.com/hg/ %s" % hg_dir)
os.chdir(hg_dir)

start = os.getcwd()
clean()

p("hg revert --all")
p("hg pull")
p("hg up -C")
if release_flag:
    p("hg up -r%s" % release_rev)

rev = p("hg tip")[-1].split()[1].replace(":", "~")
date = p("date -R")[-1]

os.rename("plugins", package)
os.chdir(package)

for release, folder in releases.iteritems():
    p("rm -R debian")
    p("cp -R ../../%s ." % folder)
    p("mv %s debian" % folder)

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

    fail(p("dpkg-buildpackage -us -uc -S -I -rfakeroot"))

p("rm -Rf debian")
os.chdir("..")
os.rename(package, "plugins")
fail(p("debsign %s*.changes %s*.dsc" % ((package,) * 2)))

dput = "dput --config '%s'" % dput_cfg
#fail(p("%s stable %s*.changes" % (dput, package)))
fail(p("%s unstable %s*.changes" % (dput, package)))
#fail(p("%s experimental %s*.changes" % (dput, package)))

clean()
