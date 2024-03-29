#!/usr/bin/env python3

import sys
import os
import urllib.parse
import html


def create_index(dir_):
    entries = sorted(os.listdir(dir_))

    links = []
    for e in entries:
        if e == "index.html":
            continue
        elif e.startswith("."):
            continue
        if os.path.isdir(os.path.join(dir_, e)):
            e += "/"
        links.append(
            "<a href='%s'>%s</a><br>" % (urllib.parse.quote(e), html.escape(e)))

    with open(os.path.join(dir_, "index.html"), "w", encoding="utf-8") as h:
        h.write("""<!DOCTYPE html>
<html>
<body>

%s

</body>
</html>""" % ("".join(links)))


def main(argv):

    def is_hidden(path):
        return any(
            (p.startswith(".") and p != "." for p in path.split(os.sep)))

    for dir_ in [l[0] for l in os.walk(argv[1]) if not is_hidden(l[0])]:
        create_index(dir_)

if __name__ == "__main__":
    main(sys.argv)
