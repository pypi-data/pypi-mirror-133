#!/usr/bin/env python3
''' test_wpa_passphrases will test challenging wpa psk passphrases

Use './test_wpa_passphrases.py --help' to see command line usage and options
Copyright 2021 Candela Technologies Inc
License: Free to distribute and modify. LANforge systems must be licensed.
 '''
import sys
import os
 

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

 
 

from lanforge_scripts.py_json.LANforge import lfcli_base
LFCliBase = lfcli_base.LFCliBase
from lanforge_scripts.py_json.LANforge import LFUtils
from lanforge_scripts.py_json.realm import Realm,PortUtils
 


class WPAPassphrases(Realm):
    def __init__(self,
                 ssid=None,
                 security=None,
                 password=None):
        self.ssid = ssid
        self.security = security
        self.password = password


def main():
    pass

if __name__ == "__main__":
    main()
