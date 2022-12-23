#!/usr/bin/env python3
import pexpect
import argparse
import subprocess
import sys
import os
import time
import datetime

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
        self.proc.sendline(f"h2 python3 generate-logs-server.py -o {output_folder} -p \"$(jobs -l)\"&")

    def run_attack(self, burst_size, burst_interval, burst_count, logs=False):
        if logs:
            self.run_server_logs(f"server-logs/s{burst_size}-c{burst_count}-t{burst_interval}".replace(".", "_"))

        # quantos bursts espacados por tempo (x segundos)
        for j in range(0, burst_count):
            # burst de pacotes (grupo de pacotes por vez)
            for i in range(0, burst_size):
                self.run_client()
            time.sleep(burst_interval)

        self.proc.expect("mininet> ", timeout=None)
        self.proc.sendline(f"h1 python3 send.py --ca-certs tests/pycacert.pem https://10.0.2.2:4433/")

    def exit(self):
        self.proc.expect("mininet> ", timeout=None)
        self.proc.sendline("exit")

def clean():
    subprocess.run(["make", "clean"])

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--burst-size", type=int, default=0)
    parser.add_argument("-c", "--burst-count", type=int, default=0)
    parser.add_argument("-t", "--burst-interval", type=float, default=0)
    return parser.parse_args()

def main():
    args = get_args()
    burst_size = args.burst_size    # workload size
    burst_count = args.burst_count
    burst_interval = args.burst_interval

    clean()
    mininet_proc = MininetProc()
    mininet_proc.run_server()

    if burst_size > 0:
        time.sleep(10) #time to open Wireshark fast
        mininet_proc.run_attack(burst_size, burst_interval, burst_count, logs=True)
    else:
        mininet_proc.run_client()

    mininet_proc.exit()

if __name__ == "__main__":
    main()
