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
    arr = raw_pid.split(" ")

    for item in arr:
        try:
            return int(item)
        except Exception as e:
            continue

    with open("server-logs/error.log", "w") as f:
        f.write("Unable to parse PID")

    raise Exception("Unable to parse PID")


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
        mem_info = p.memory_info()
        mem_p = p.memory_percent()
        cpu_p = p.cpu_percent()
        is_run = p.is_running()
        now = str(dt.now())

        mem_data = {
            "timestamp": now,
            "is_running": is_run,
            "rss": mem_info.rss,
            "vms": mem_info.vms,
            "percent": mem_p
        }

        cpu_data = {
            "timestamp": now,
            "is_running": is_run,
            "percent": cpu_p
        }

        save(f"{output_folder}/server-mem.json", mem_data)
        save(f"{output_folder}/server-cpu.json", cpu_data)
        #save(f"{output_folder}/server-net.json", net_data)
        time.sleep(0.5)

if __name__ == "__main__":
    main()
