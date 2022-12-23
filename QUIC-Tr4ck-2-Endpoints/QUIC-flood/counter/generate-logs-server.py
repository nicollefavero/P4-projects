#!/usr/bin/env python3
import psutil
import argparse
import json
import time
import os
from datetime import datetime as dt

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output-folder", type=str, default="server-logs")
    parser.add_argument("-p", "--raw-pid", type=str, default="")
    return parser.parse_args()


def parse_pid(raw_pid):
    return int(raw_pid.split(" ")[1])


def save(filepath, data):
    with open(filepath, "a") as json_file:
        json.dump(data, json_file, indent=4)
        json_file.write(",\n")


def main():
    args = get_args()
    output_folder = args.output_folder
    pid = parse_pid(args.raw_pid)

    p = psutil.Process(pid)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for x in range(200):
        mem = psutil.virtual_memory()
        cpu_p = psutil.cpu_percent()
        net = psutil.net_io_counters()
        now = str(dt.now())

        mem_data = {
            "timestamp": now,
            "total": mem.total,
            "available": mem.available,
            "percent": mem.percent,
            "used": mem.used,
            "free": mem.free
        }

        cpu_data = {
            "timestamp": now,
            "percent": cpu_p
        }

        net_data = {
            "timestamp": now,
            "bytes_recv": net.bytes_recv,
            "packets_recv": net.packets_recv
        }

        save(f"{output_folder}/server-mem.json", mem_data)
        save(f"{output_folder}/server-cpu.json", cpu_data)
        save(f"{output_folder}/server-net.json", net_data)
        time.sleep(0.5)

if __name__ == "__main__":
    main()
