#!/usr/bin/env python3
"""
This example is to demonstrate ws_generic_monitor to monitor events triggered by scripts,
This script when running, will monitor the events triggered by test_ipv4_connection.py

"""
import sys
import os
 

 
 

from lanforge_scripts.py_json import ws_generic_monitor
WS_Listener = ws_generic_monitor.WS_Listener
from lanforge_scripts.py_json.realm import Realm,PortUtils
 

reference = "test_ipv4_connection.py"


class GenericMonitorTest(Realm):
    def __init__(self,
                 ssid=None,
                 security=None,
                 password=None,
                 radio=None):
        self.ssid=ssid
        self.security=security
        self.password=password
        self.radio=radio

    def start(self):
        pass

    def stop(self):
        pass

    def monitor(self):
        pass

def main():
    WS_Listener(lfclient_host="localhost", _scriptname=reference)#, _callback=TestRun)


if __name__ == "__main__":
    main()

