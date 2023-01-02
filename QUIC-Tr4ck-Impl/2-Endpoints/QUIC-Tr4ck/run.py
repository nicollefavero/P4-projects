#!/usr/bin/env python3
import pexpect
import argparse
import subprocess
import sys
import os
import time
import datetime

MAKEFILE_PATH = "/home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck/p4-src/Makefile"
SCRIPTS_PATH = "/home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/2-Endpoints/QUIC-Tr4ck"

class MininetProc:
    def __init__(self) -> None:
        self.proc = pexpect.spawn("make run", cwd=os.path.dirname(MAKEFILE_PATH), encoding="utf-8")
        self.proc.logfile_read = sys.stdout

    def run_server(self, logs=False, output_folder=None):
        self.proc.expect("mininet> ", timeout=None)
        self.proc.sendline(f"h2 {SCRIPTS_PATH}/run-server.sh &")

        if logs:
            self.proc.expect("mininet> ", timeout=None)
            self.proc.sendline(f"h2 python3 {SCRIPTS_PATH}/generate-server-logs.py -o {output_folder}/baseline -p \"$(jobs -l)\"")

    def run_client(self):
        self.proc.expect("mininet> ", timeout=None)
        self.proc.sendline(f"h1 {SCRIPTS_PATH}/run-client.sh &")

    def run_server_logs(self, output_folder):
        self.proc.expect("mininet> ", timeout=None)
        self.proc.sendline(f"h2 python3 {SCRIPTS_PATH}/generate-server-logs.py -o {output_folder} -p \"$(jobs -l)\" &")

    def run_attack(self, output_folder, burst_size, burst_interval, burst_count, logs=False):
        if logs:
            self.run_server_logs(f"{output_folder}/s{burst_size}-c{burst_count}-t{burst_interval}".replace(".", "_"))

        time.sleep(10)
        # quantos bursts espacados por tempo (x segundos)
        for j in range(0, burst_count):
            # burst de pacotes (grupo de pacotes por vez)
            for i in range(0, burst_size):
                self.run_client()
            time.sleep(burst_interval)

        self.proc.expect("mininet> ", timeout=None)
        self.proc.sendline(f"h1 {SCRIPTS_PATH}/run-client.sh")

    def exit(self):
        self.proc.expect("mininet> ", timeout=None)
        self.proc.sendline("exit")

def clean():
    subprocess.run(["make", "clean"], cwd=os.path.dirname(MAKEFILE_PATH))

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--burst-size", type=int, default=0)
    parser.add_argument("-c", "--burst-count", type=int, default=0)
    parser.add_argument("-t", "--burst-interval", type=float, default=0)
    parser.add_argument("-o", "--output-folder", type=str, default=f"{SCRIPTS_PATH}/server-logs")
    return parser.parse_args()

def main():
    args = get_args()
    burst_size = args.burst_size    # workload size
    burst_count = args.burst_count
    burst_interval = args.burst_interval
    output_folder = args.output_folder

    clean()
    mininet_proc = MininetProc()

    if burst_size > 0:
        mininet_proc.run_server()
        #time.sleep(5)
        mininet_proc.run_attack(output_folder, burst_size, burst_interval, burst_count, logs=True)
    else:
        mininet_proc.run_server()

    mininet_proc.exit()

if __name__ == "__main__":
    main()
