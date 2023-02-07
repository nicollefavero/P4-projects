#!/usr/bin/env python3
import pexpect
import argparse
import subprocess
import sys
import os
import time
import datetime

MAKEFILE_PATH = "/home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-flood/p4-src/Makefile"
SCRIPTS_PATH = "/home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-flood"

class MininetProc:
    def __init__(self) -> None:
        self.proc = pexpect.spawn("make run", cwd=os.path.dirname(MAKEFILE_PATH), encoding="utf-8")
        self.proc.logfile_read = sys.stdout

    def run_server(self, logs=False, output_folder=None):
        self.proc.expect("mininet> ", timeout=None)
        self.proc.sendline(f"h2 python3 {SCRIPTS_PATH}/quic-src/receive.py --certificate {SCRIPTS_PATH}/quic-src/tests/ssl_cert.pem --private-key {SCRIPTS_PATH}/quic-src/tests/ssl_key.pem &")

    def run_client(self):
        self.proc.expect("mininet> ", timeout=None)
        self.proc.sendline(f"h1 python3 {SCRIPTS_PATH}/quic-src/send.py --ca-certs {SCRIPTS_PATH}/quic-src/tests/pycacert.pem https://10.0.2.2:4433/ &")

    def exit(self):
        self.proc.expect("mininet> ", timeout=None)
        self.proc.sendline("exit")

def clean():
    subprocess.run(["make", "clean"], cwd=os.path.dirname(MAKEFILE_PATH))

def main():

    clean()
    mininet_proc = MininetProc()
    mininet_proc.run_server()
    mininet_proc.run_client()
    mininet_proc.exit()

if __name__ == "__main__":
    main()
