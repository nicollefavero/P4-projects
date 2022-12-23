import json
import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
import datetime
import numpy as np
import argparse

FLOOD_PATH = "./QUIC-flood"
TR4CK_PATH = "./QUIC-Tr4ck"
BASELINE_PATH = "./baseline"
TYPE = "cpu"
ATTR = "percent"

def load_metrics(project_path, test_case, resource):
    with open(f"{project_path}/{test_case}/server-{resource}.json", "r") as json_file:
        full_logs = "[" + json_file.read()[:-2] + "]"
        return (json.loads(full_logs))

def load_baseline(resource):
    with open(f"./baseline/server-{resource}.json", "r") as json_file:
        a = json_file.read()
        full_logs = "[" + a[:-2] + "]"
        return json.loads(full_logs)

def get_data_to_plot(data, label):
    arr = []
    for item in data:
        arr.append(item[label])
    return arr

def get_times_to_plot(data):
    first = datetime.datetime.strptime(data[0]["timestamp"], '%Y-%m-%d %H:%M:%S.%f')
    last = datetime.datetime.strptime(data[-1]["timestamp"], '%Y-%m-%d %H:%M:%S.%f')
    diff = (last - first).total_seconds()

    arr = np.linspace(0, diff, len(data))
    return arr

def main():
    #args = get_args()
    #test_cases = args.cases

    # Baseline Data
    b_data = load_baseline(TYPE)

    # Flood data
    f_data_s2c2 = load_metrics(FLOOD_PATH, "s2-c2-t1_0", TYPE)
    f_data_s4c2 = load_metrics(FLOOD_PATH, "s4-c2-t1_0", TYPE)
    f_data_s8c2 = load_metrics(FLOOD_PATH, "s8-c2-t1_0", TYPE)

    f_data_s2c4 = load_metrics(FLOOD_PATH, "s2-c4-t1_0", TYPE)
    f_data_s4c4 = load_metrics(FLOOD_PATH, "s4-c4-t1_0", TYPE)
    f_data_s8c4 = load_metrics(FLOOD_PATH, "s8-c4-t1_0", TYPE)

    f_data_s2c8 = load_metrics(FLOOD_PATH, "s2-c8-t1_0", TYPE)
    f_data_s4c8 = load_metrics(FLOOD_PATH, "s4-c8-t1_0", TYPE)
    f_data_s8c8 = load_metrics(FLOOD_PATH, "s8-c8-t1_0", TYPE)

    # Tr4ck data
    t_data_s2c2 = load_metrics(TR4CK_PATH, "s2-c2-t1_0", TYPE)
    t_data_s4c2 = load_metrics(TR4CK_PATH, "s4-c2-t1_0", TYPE)
    t_data_s8c2 = load_metrics(TR4CK_PATH, "s8-c2-t1_0", TYPE)

    t_data_s2c4 = load_metrics(TR4CK_PATH, "s2-c4-t1_0", TYPE)
    t_data_s4c4 = load_metrics(TR4CK_PATH, "s4-c4-t1_0", TYPE)
    t_data_s8c4 = load_metrics(TR4CK_PATH, "s8-c4-t1_0", TYPE)

    t_data_s2c8 = load_metrics(TR4CK_PATH, "s2-c8-t1_0", TYPE)
    t_data_s4c8 = load_metrics(TR4CK_PATH, "s4-c8-t1_0", TYPE)
    t_data_s8c8 = load_metrics(TR4CK_PATH, "s8-c8-t1_0", TYPE)

    # Baseline - Data in the axes
    print("baseline")
    b_xdata = get_times_to_plot(b_data)
    b_ydata = get_data_to_plot(b_data, ATTR)

    # Flood - Data in the axes
    print("flood")
    f_xdata_s2c2 = get_times_to_plot(f_data_s2c2)
    f_ydata_s2c2 = get_data_to_plot(f_data_s2c2, ATTR)
    f_xdata_s4c2 = get_times_to_plot(f_data_s4c2)
    f_ydata_s4c2 = get_data_to_plot(f_data_s4c2, ATTR)
    f_xdata_s8c2 = get_times_to_plot(f_data_s8c2)
    f_ydata_s8c2 = get_data_to_plot(f_data_s8c2, ATTR)

    f_xdata_s2c4 = get_times_to_plot(f_data_s2c4)
    f_ydata_s2c4 = get_data_to_plot(f_data_s2c4, ATTR)
    f_xdata_s4c4 = get_times_to_plot(f_data_s4c4)
    f_ydata_s4c4 = get_data_to_plot(f_data_s4c4, ATTR)
    f_xdata_s8c4 = get_times_to_plot(f_data_s8c4)
    f_ydata_s8c4 = get_data_to_plot(f_data_s8c4, ATTR)

    f_xdata_s2c8 = get_times_to_plot(f_data_s2c8)
    f_ydata_s2c8 = get_data_to_plot(f_data_s2c8, ATTR)
    f_xdata_s4c8 = get_times_to_plot(f_data_s4c8)
    f_ydata_s4c8 = get_data_to_plot(f_data_s4c8, ATTR)
    f_xdata_s8c8 = get_times_to_plot(f_data_s8c8)
    f_ydata_s8c8 = get_data_to_plot(f_data_s8c8, ATTR)

    # Tr4ck - Data in the axes
    print("tr4ck")
    t_xdata_s2c2 = get_times_to_plot(t_data_s2c2)
    t_ydata_s2c2 = get_data_to_plot(t_data_s2c2, ATTR)
    t_xdata_s4c2 = get_times_to_plot(t_data_s4c2)
    t_ydata_s4c2 = get_data_to_plot(t_data_s4c2, ATTR)
    t_xdata_s8c2 = get_times_to_plot(t_data_s8c2)
    t_ydata_s8c2 = get_data_to_plot(t_data_s8c2, ATTR)

    t_xdata_s2c4 = get_times_to_plot(t_data_s2c4)
    t_ydata_s2c4 = get_data_to_plot(t_data_s2c4, ATTR)
    t_xdata_s4c4 = get_times_to_plot(t_data_s4c4)
    t_ydata_s4c4 = get_data_to_plot(t_data_s4c4, ATTR)
    t_xdata_s8c4 = get_times_to_plot(t_data_s8c4)
    t_ydata_s8c4 = get_data_to_plot(t_data_s8c4, ATTR)

    t_xdata_s2c8 = get_times_to_plot(t_data_s2c8)
    t_ydata_s2c8 = get_data_to_plot(t_data_s2c8, ATTR)
    t_xdata_s4c8 = get_times_to_plot(t_data_s4c8)
    t_ydata_s4c8 = get_data_to_plot(t_data_s4c8, ATTR)
    t_xdata_s8c8 = get_times_to_plot(t_data_s8c8)
    t_ydata_s8c8 = get_data_to_plot(t_data_s8c8, ATTR)


    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.plot(b_xdata, b_ydata)

    ax.plot(f_xdata_s2c2, f_ydata_s2c2)
    #ax.plot(f_xdata_s4c2, f_ydata_s4c2)
    #ax.plot(f_xdata_s8c2, f_ydata_s8c2)

    #ax.plot(f_xdata_s2c4, f_ydata_s2c4)
    #ax.plot(f_xdata_s4c4, f_ydata_s4c4)
    #ax.plot(f_xdata_s8c4, f_ydata_s8c4)

    #ax.plot(f_xdata_s2c8, f_ydata_s2c8)
    #ax.plot(f_xdata_s4c8, f_ydata_s4c8)
    #ax.plot(f_xdata_s8c8, f_ydata_s8c8)

    ax.plot(t_xdata_s2c2, t_ydata_s2c2)
    #ax.plot(t_xdata_s4c2, t_ydata_s4c2)
    #ax.plot(t_xdata_s8c2, t_ydata_s8c2)

    #ax.plot(t_xdata_s2c4, t_ydata_s2c4)
    #ax.plot(t_xdata_s4c4, t_ydata_s4c4)
    #ax.plot(t_xdata_s8c4, t_ydata_s8c4)

    #ax.plot(t_xdata_s2c8, t_ydata_s2c8)
    #ax.plot(t_xdata_s4c8, t_ydata_s4c8)
    #ax.plot(t_xdata_s8c8, t_ydata_s8c8)

    plt.legend(["Baseline",
                "Control",
                "QUIC-Tr4ck"], loc="lower right")

    plt.ylabel(f'{TYPE} {ATTR}', fontsize=16)
    plt.xlabel('time (s)', fontsize=16)

    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)

    # Baseline events
    b_xevents = EventCollection(b_xdata, linelength=0.05)
    b_xevents = EventCollection(b_ydata, linelength=0.05)

    # Flood events
    f_xevents_s2c2 = EventCollection(f_xdata_s2c2, linelength=0.05)
    #f_xevents_s4c2 = EventCollection(f_xdata_s4c2, linelength=0.05)
    #f_xevents_s8c2 = EventCollection(f_xdata_s8c2, linelength=0.05)

    f_yevents_s2c2 = EventCollection(f_ydata_s2c2, linelength=0.05)
    #f_yevents_s4c2 = EventCollection(f_ydata_s4c2, linelength=0.05)
    #f_yevents_s8c2 = EventCollection(f_ydata_s8c2, linelength=0.05)

    #f_xevents_s2c4 = EventCollection(f_xdata_s2c4, linelength=0.05)
    #f_xevents_s4c4 = EventCollection(f_xdata_s4c4, linelength=0.05)
    #f_xevents_s8c4 = EventCollection(f_xdata_s8c4, linelength=0.05)

    #f_yevents_s2c4 = EventCollection(f_ydata_s2c4, linelength=0.05)
    #f_yevents_s4c4 = EventCollection(f_ydata_s4c4, linelength=0.05)
    #f_yevents_s8c4 = EventCollection(f_ydata_s8c4, linelength=0.05)

    #f_xevents_s2c8 = EventCollection(f_xdata_s2c8, linelength=0.05)
    #f_xevents_s4c8 = EventCollection(f_xdata_s4c8, linelength=0.05)
    #f_xevents_s8c8 = EventCollection(f_xdata_s8c8, linelength=0.05)

    #f_yevents_s2c8 = EventCollection(f_ydata_s2c8, linelength=0.05)
    #f_yevents_s4c8 = EventCollection(f_ydata_s4c8, linelength=0.05)
    #f_yevents_s8c8 = EventCollection(f_ydata_s8c8, linelength=0.05)

    # Tr4ck events
    t_xevents_s2c2 = EventCollection(t_xdata_s2c2, linelength=0.05)
    #t_xevents_s4c2 = EventCollection(t_xdata_s4c2, linelength=0.05)
    #t_xevents_s8c2 = EventCollection(t_xdata_s8c2, linelength=0.05)

    t_yevents_s2c2 = EventCollection(t_ydata_s2c2, linelength=0.05)
    #t_yevents_s4c2 = EventCollection(t_ydata_s4c2, linelength=0.05)
    #t_yevents_s8c2 = EventCollection(t_ydata_s8c2, linelength=0.05)

    #t_xevents_s2c4 = EventCollection(t_xdata_s2c4, linelength=0.05)
    #t_xevents_s4c4 = EventCollection(t_xdata_s4c4, linelength=0.05)
    #t_xevents_s8c4 = EventCollection(t_xdata_s8c4, linelength=0.05)

    #t_yevents_s2c4 = EventCollection(t_ydata_s2c4, linelength=0.05)
    #t_yevents_s4c4 = EventCollection(t_ydata_s4c4, linelength=0.05)
    #t_yevents_s8c4 = EventCollection(t_ydata_s8c4, linelength=0.05)

    #t_xevents_s2c8 = EventCollection(t_xdata_s2c8, linelength=0.05)
    #t_xevents_s4c8 = EventCollection(t_xdata_s4c8, linelength=0.05)
    #t_xevents_s8c8 = EventCollection(t_xdata_s8c8, linelength=0.05)
#
    #t_yevents_s2c8 = EventCollection(t_ydata_s2c8, linelength=0.05)
    #t_yevents_s4c8 = EventCollection(t_ydata_s4c8, linelength=0.05)
    #t_yevents_s8c8 = EventCollection(t_ydata_s8c8, linelength=0.05)

    # Add events
    ax.add_collection(b_xevents)
    ax.add_collection(b_xevents)

    ax.add_collection(f_xevents_s2c2)
    #ax.add_collection(f_xevents_s4c2)
    #ax.add_collection(f_xevents_s8c2)

    ax.add_collection(f_yevents_s2c2)
    #ax.add_collection(f_yevents_s4c2)
    #ax.add_collection(f_yevents_s8c2)

    #ax.add_collection(f_xevents_s2c4)
    #ax.add_collection(f_xevents_s4c4)
    #ax.add_collection(f_xevents_s8c4)

    #ax.add_collection(f_yevents_s2c4)
    #ax.add_collection(f_yevents_s4c4)
    #ax.add_collection(f_yevents_s8c4)

    #ax.add_collection(f_xevents_s2c8)
    #ax.add_collection(f_xevents_s4c8)
    #ax.add_collection(f_xevents_s8c8)

    #ax.add_collection(f_yevents_s2c8)
    #ax.add_collection(f_yevents_s4c8)
    #ax.add_collection(f_yevents_s8c8)

    ax.add_collection(t_xevents_s2c2)
    #ax.add_collection(t_xevents_s4c2)
    #ax.add_collection(t_xevents_s8c2)

    ax.add_collection(t_yevents_s2c2)
    #ax.add_collection(t_yevents_s4c2)
    #ax.add_collection(t_yevents_s8c2)

    #ax.add_collection(t_xevents_s2c4)
    #ax.add_collection(t_xevents_s4c4)
    #ax.add_collection(t_xevents_s8c4)

    #ax.add_collection(t_yevents_s2c4)
    #ax.add_collection(t_yevents_s4c4)
    #ax.add_collection(t_yevents_s8c4)

    #ax.add_collection(t_xevents_s2c8)
    #ax.add_collection(t_xevents_s4c8)
    #ax.add_collection(t_xevents_s8c8)

    #ax.add_collection(t_yevents_s2c8)
    #ax.add_collection(t_yevents_s4c8)
    #ax.add_collection(t_yevents_s8c8)


    plt.savefig(f"s2c2-{TYPE}.pdf")
    plt.show()

if __name__=="__main__":
    main()
