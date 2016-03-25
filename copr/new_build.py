#!/usr/bin/python2

import requests
import ConfigParser
from requests.auth import HTTPBasicAuth
import sys
import os


def main(argv):
    srpm_url = argv[1]

    dir_ = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser.RawConfigParser()
    config_path = os.path.join(dir_, "copr.conf")
    assert os.path.exists(config_path), "%s missing. Visit https://copr.fedorainfracloud.org/api/" % config_path

    config.read(config_path)
    username = config.get("copr-cli", "login")
    token = config.get("copr-cli", "token")

    url = "http://copr.fedoraproject.org/api/coprs/lazka/quodlibet-unstable/new_build/"
    args = {
        "pkgs": srpm_url,
    }
    r = requests.post(url, auth=HTTPBasicAuth(username, token), data=args)
    print r.text


if __name__ == "__main__":
    main(sys.argv)
