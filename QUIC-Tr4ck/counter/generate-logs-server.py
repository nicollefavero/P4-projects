import psutil
import argparse
import json

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--request-index", type=int, default=1) # client request index to log
    parser.add_argument("-o", "--output-folder", type=str, default="server-logs")
    return parser.parse_args()


def save(filepath, data):
    with open(filepath, "a") as json_file:
        json.dump(data, json_file, indent=4)
        json_file.write(",\n")


def main():
    args = get_args()
    idx = args.request_index
    output_folder = args.output_folder

    mem = psutil.virtual_memory()
    cpu_f = psutil.cpu_freq()
    cpu_p = psutil.cpu_percent()
    net = psutil.net_io_counters()

    mem_data = {
        "request_index": idx,
        "total": mem.total,
        "available": mem.available,
        "percent": mem.percent,
        "used": mem.used,
        "free": mem.free
    }

    cpu_data = {
        "request_index": idx,
        "percent": cpu_p,
        "frequency": cpu_f.current,
        "min_frequency": cpu_f.min,
        "max_frequency": cpu_f.max
    }

    net_data = {
        "request_index": idx,
        "bytes_recv": net.bytes_recv,
        "packets_recv": net.packets_recv,
        "dropin": net.dropin
    }

    save(f"{output_folder}/server-mem.json", mem_data)
    save(f"{output_folder}/server-cpu.json", cpu_data)
    save(f"{output_folder}/server-net.json", net_data)

if __name__ == "__main__":
    main()
