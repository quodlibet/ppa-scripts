#!/usr/bin/python
# Copyright 2013 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import os.path
import paramiko
import getpass

###############################################################################

HOST = "pluto.tugraz.at"
PORT = 22
LOCAL = "~/debian_archive/quodlibet-unstable"
REMOTE = "/mnt/dfs/christoph_reiter/app/WWW/christoph_reiter/debian/quodlibet-unstable"

###############################################################################

print "%s:%d" % (HOST, PORT)

while 1:
    username = getpass.getpass("user:")
    password = getpass.getpass("passwd:")

    t = paramiko.Transport((HOST, PORT))

    try:
        t.connect(username=username, password=password)
    except paramiko.AuthenticationException:
        print "auth failed"
        t.close()
    else:
        break

sftp = paramiko.SFTPClient.from_transport(t)

for part in os.path.split(REMOTE):
    sftp.chdir(part)

for file_ in sftp.listdir('.'):
    print "removing: %r" % file_
    sftp.remove(file_)

LOCAL = os.path.expanduser(LOCAL)
new_files = os.listdir(LOCAL)
assert len(new_files) > 10
for new in new_files:
    new_path = os.path.join(LOCAL, new)
    print "uploading: %r" %new
    sftp.put(new_path, new)

t.close()
