import json
import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
import datetime
import numpy as np

FLOOD_PATH = "./QUIC-flood"
TR4CK_PATH = "./QUIC-Tr4ck"

def load_metrics(project_path, test_case, resource):
    with open(f"{project_path}/{test_case}/server-{resource}.json", "r") as json_file:
        return json.load(json_file)

def get_data_to_plot(data, label):
    arr = []
    for item in data:
        arr.append(item[label])
    return arr

def get_timestamps(data):
    first = datetime.datetime.strptime(data[0]["timestamp"], '%Y-%m-%d %H:%M:%S.%f')
    last = datetime.datetime.strptime(data[-1]["timestamp"], '%Y-%m-%d %H:%M:%S.%f')
    diff = (last - first).total_seconds() * 1000 # milisseconds

    arr = np.linspace(0, diff, len(data))
    return arr

def main():
    flood_data_mem_s2 = load_metrics(FLOOD_PATH, "s2-c4-t1_0", "mem")
    tr4ck_data_mem_s2 = load_metrics(TR4CK_PATH, "s2-c4-t1_0", "mem")

    xdata_flood = get_timestamps(flood_data_mem_s2)
    ydata_flood = get_data_to_plot(flood_data_mem_s2, "percent")

    xdata_tr4ck = get_timestamps(tr4ck_data_mem_s2)
    ydata_tr4ck = get_data_to_plot(tr4ck_data_mem_s2, "percent")

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(xdata_flood, ydata_flood, color='tab:red')
    ax.plot(xdata_tr4ck, ydata_tr4ck, color='tab:green')

    plt.legend(["Baseline", "QUIC-Tr4ck"], loc="lower right")

    plt.ylabel('% memory', fontsize=16)
    plt.xlabel('time (s)', fontsize=16)

    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)

    xevents_flood = EventCollection(xdata_flood, color='tab:red', linelength=0.05)
    xevents_tr4ck = EventCollection(xdata_tr4ck, color='tab:green', linelength=0.05)

    yevents_flood = EventCollection(ydata_flood, color='tab:red', linelength=0.05)
    yevents_tr4ck = EventCollection(ydata_tr4ck, color='tab:green', linelength=0.05)

    ax.add_collection(xevents_flood)
    ax.add_collection(xevents_tr4ck)
    ax.add_collection(yevents_flood)
    ax.add_collection(yevents_tr4ck)

    plt.savefig("s2-c4-t1_0-MEM.pdf")
    plt.show()

if __name__=="__main__":
    main()
