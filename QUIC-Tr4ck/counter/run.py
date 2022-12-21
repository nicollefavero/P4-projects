#!/usr/bin/env python3
import pexpect
import psutil
import argparse
import subprocess
import sys
import os
import time

class MininetProc:
    def __init__(self) -> None:
        self.proc = pexpect.spawn("make run", encoding="utf-8")
        self.proc.logfile_read = sys.stdout

    def run_server(self):
        self.proc.expect("mininet> ", timeout=None)
        self.proc.sendline("h2 python3 receive.py --certificate tests/ssl_cert.pem --private-key tests/ssl_key.pem &")

    def run_client(self):
        self.proc.expect("mininet> ", timeout=None)
        self.proc.sendline(f"h1 python3 send.py --ca-certs tests/pycacert.pem https://10.0.2.2:4433/")

    def __run_client(self):
        self.proc.expect("mininet> ", timeout=None)
        self.proc.sendline(f"h1 python3 send.py --ca-certs tests/pycacert.pem https://10.0.2.2:4433/ &")

    def run_server_logs(self, request_index):
        self.proc.expect("mininet> ", timeout=None)
        self.proc.sendline(f"h2 python3 generate-logs-server.py -r {request_index}")

    def run_attack(self, workload_size, logs=False):
        for i in range(workload_size):
            self.__run_client()

            if logs:
                self.run_server_logs(i)

    def exit(self):
        self.proc.expect("mininet> ", timeout=None)
        self.proc.sendline("exit")

def clean():
    subprocess.run(["make", "clean"])

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--attack", type=int, default=0)
    return parser.parse_args()

def main():
    args = get_args()
    workload_size = args.attack

    clean()
    mininet_proc = MininetProc()
    mininet_proc.run_server()

    if workload_size > 0:
        mininet_proc.run_attack(workload_size, logs=True)
    else:
        mininet_proc.run_client()

    mininet_proc.exit()

if __name__ == "__main__":
    main()
