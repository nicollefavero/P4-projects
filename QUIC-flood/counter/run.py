#!/usr/bin/env python3
import pexpect
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
        self.proc.sendline(f"h1 python3 send.py --ca-certs tests/pycacert.pem https://10.0.2.2:4433/ &")

    def run_server_logs(self, output_folder):
        self.proc.expect("mininet> ", timeout=None)
        self.proc.sendline(f"h2 python3 generate-logs-server.py -o {output_folder} &")

    def run_attack(self, workload_size, output_folder, logs=False):
        if logs:
            self.run_server_logs(output_folder)

        for i in range(workload_size):
            self.run_client()

        self.proc.expect("mininet> ", timeout=None)
        self.proc.sendline(f"h1 python3 send.py --ca-certs tests/pycacert.pem https://10.0.2.2:4433/")

    def exit(self):
        self.proc.expect("mininet> ", timeout=None)
        self.proc.sendline("exit")

def clean():
    subprocess.run(["make", "clean"])

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--attack", type=int, default=0)
    parser.add_argument("-o", "--output-folder", type=str, default="server-logs")
    return parser.parse_args()

def main():
    args = get_args()
    workload_size = args.attack
    output_folder = args.output_folder

    clean()
    mininet_proc = MininetProc()
    mininet_proc.run_server()

    if workload_size > 0:
        mininet_proc.run_attack(workload_size, output_folder, logs=True)
    else:
        mininet_proc.run_client()

    mininet_proc.exit()

if __name__ == "__main__":
    main()
