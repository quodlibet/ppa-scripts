#!/usr/bin/env python

from optparse import OptionParser
import subprocess
import sys
import os

def parse_args():
    parser = OptionParser()
    parser.add_option("-r", "--release", dest="release", action="store_true",
                      default=False, help="stable release")

    parser.add_option("--py3", dest="py3", action="store_true",
                      default=False, help="py3")

    parser.add_option("-d", "--dist", action="store", dest="dist",
                      default="ubuntu", help="ubuntu/debian",
                      choices=["ubuntu", "debian"])

    parser.add_option("-v", "--version", action="store", dest="version",
                      default=0, type="int", help="version increment")

    return parser.parse_args()[0]

def cd(d):
    old = os.getcwd()
    os.chdir(d)
    print "> CD: %s -> %s" % (old, d)

def p(cmd):
    print "> %s" % cmd
    pipe = subprocess.PIPE
    p = subprocess.Popen(cmd, shell=True, stdout=pipe, stderr=pipe, stdin=pipe)
    stdout, stderr = p.communicate()
    return p.returncode, stdout.strip(), stderr.strip()

def clean(directory, *packages):
    old = os.getcwd()
    os.chdir(directory)
    for package in packages:
        cmd = "rm %s*.changes %s*.tar.gz %s*.tar.xz %s*.dsc %s*.upload %s*.deb %s*.build %s*.buildinfo %s*.diff.gz" % ((package,) * 9)
        p(cmd)
    os.chdir(old)

def fail(out):
    status, stdout, stderr = out
    if status != 0:
        print "#" * 24
        print stdout
        print stderr
        print "#" * 24
        sys.exit()
    return out
