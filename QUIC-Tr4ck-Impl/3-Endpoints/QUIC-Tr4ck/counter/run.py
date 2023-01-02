#!/usr/bin/env python3
import pexpect
import argparse
import subprocess
import sys
import os
import time
import datetime

def generate_request_time_log(times, interval, num_requests, burst_size, burst_interval, burst_count):
    with open(f"client-logs/time-{num_requests}-{interval}-s{burst_size}-c{burst_count}-t{burst_interval}.log".split(".", "_"), "a") as file:
        for time in times:
            file.write(time)
            file.write("\n")


class MininetProc:
    def __init__(self) -> None:
        self.proc = pexpect.spawn("make run", encoding="utf-8")
        self.proc.logfile_read = sys.stdout

    def run_server(self, logs=False):
        self.proc.expect("mininet> ", timeout=None)
        self.proc.sendline("h2 python3 receive.py --certificate tests/ssl_cert.pem --private-key tests/ssl_key.pem &")

        if logs:
            self.proc.expect("mininet> ", timeout=None)
            self.proc.sendline(f"h2 python3 generate-logs-server.py -o server-logs/baseline -p \"$(jobs -l)\"")

    def run_client(self, interval, num_requests, logs=False, burst_size, burst_interval, burst_count):
        self.proc.expect("mininet> ", timeout=None)

        conn_times = []
        for i in range(num_requests):
            t_start = time.start()
            self.proc.sendline(f"h3 python3 send.py --ca-certs tests/pycacert.pem https://10.0.2.2:4433/")
            t_end = time.end()

            conn_times.append(t_end - t_start)
            time.sleep(interval)

        if logs:
            generate_request_time_log(conn_times, interval, num_requests, burst_size, burst_interval, burst_count)

    def run_server_logs(self, output_folder):
        self.proc.expect("mininet> ", timeout=None)
        self.proc.sendline(f"h2 python3 generate-logs-server.py -o {output_folder} -p \"$(jobs -l)\" &")

    def run_attack(self, burst_size, burst_interval, burst_count, logs=False):
        if logs:
            self.run_server_logs(f"server-logs/s{burst_size}-c{burst_count}-t{burst_interval}".replace(".", "_"))

        # quantos bursts espacados por tempo (x segundos)
        for j in range(0, burst_count):
            # burst de pacotes (grupo de pacotes por vez)
            for i in range(0, burst_size):
                self.proc.sendline(f"h1 python3 send.py --ca-certs tests/pycacert.pem https://10.0.2.2:4433/")
            time.sleep(burst_interval)

        self.proc.expect("mininet> ", timeout=None)
        self.proc.sendline(f"h1 python3 send.py --ca-certs tests/pycacert.pem https://10.0.2.2:4433/ &")

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
    parser.add_argument("-r", "--requests-number", type=int, default=1)
    parser.add_argument("-i", "--interval", type=int, default=0)
    return parser.parse_args()

def main():
    args = get_args()
    burst_size = args.burst_size    # workload size
    burst_count = args.burst_count
    burst_interval = args.burst_interval
    num_requests = args.requests_number
    interval = args.interval

    clean()
    mininet_proc = MininetProc()

    if burst_size > 0:
        mininet_proc.run_server()
        time.sleep(10)
        mininet_proc.run_attack(burst_size, burst_interval, burst_count)
        mininet_proc.run_client(interval, num_requests, logs=True, burst_size, burst_interval, burst_count)
    else:
        mininet_proc.run_server(logs=True)

    mininet_proc.exit()

if __name__ == "__main__":
    main()