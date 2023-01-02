import json
import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
import datetime
import numpy as np
import argparse
import random
import os

FLOOD_PATH = "./QUIC-flood/test_01"
TR4CK_PATH = "./QUIC-Tr4ck/test_01"

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--flood", action="store_true")
    parser.add_argument("-k", "--track", action="store_true")
    parser.add_argument("-i", "--input-files", type=str, nargs='+')
    parser.add_argument("-r", "--resource", type=str, default="mem")
    parser.add_argument("-a", "--attribute", type=str, default="percent")
    parser.add_argument("-o", "--output-file", type=str, default="")
    #parser.add_argument("-b", "--baseline", action="store_false")
    parser.add_argument("-s", action="store_true")
    parser.add_argument("-c", action="store_true")
    parser.add_argument("-t", action="store_true")
    return parser.parse_args()


def __load_metrics(project_path, test_case, resource):
    with open(f"{project_path}/{test_case}/server-{resource}.json", "r") as json_file:
        full_logs = "[" + json_file.read()[:-2] + "]"
        return (json.loads(full_logs))

def __load_baseline(resource):
    with open(f"./baseline/server-{resource}.json", "r") as json_file:
        a = json_file.read()
        full_logs = "[" + a[:-2] + "]"
        return json.loads(full_logs)


def __get_data_to_plot(data, label):
    arr = []
    for item in data:
        arr.append(item[label])
    return arr


def __get_times_to_plot(data):
    first = datetime.datetime.strptime(data[0]["timestamp"], '%Y-%m-%d %H:%M:%S.%f')
    last = datetime.datetime.strptime(data[-1]["timestamp"], '%Y-%m-%d %H:%M:%S.%f')
    diff = (last - first).total_seconds()

    arr = np.linspace(0, diff, len(data))
    return arr

# Only works with 1 varying parameter
def __get_varying_metric(input, s, c, t):
    arr = input.split("-")
    s_idx = ""
    c_idx = ""
    t_idx = ""

    if s:
        s_idx = arr[0][1:]
        return s_idx
    if c:
        c_idx = arr[1][1:]
        return c_idx
    if t:
        t_idx = arr[2][1:].replace("_", ".")
        return t_idx


def __colors():
    return [
        "#DC143C", #crimson
        "#808000", #olive
        "#008B8B", #dark cyan
        "#48D1CC", #medium turquoise
        "#A52A2A", #brown
        "#FFA500", #orange
        "#663399", #rebecca purple
        "#32CD32", #lime green
        "#3CB371", #medium sea green
        "#DA70D6", #orchid
        "#800000", #maroon
        "#0000FF", #blue
        "#8B4513", #saddle brown
        "#FF0000", #red
        "#8B0000", #dark red
        "#FF1493", #deep pink
        "#C71585", #medium violet red
        "#FF4500", #orange red
        "#8B008B", #dark magenta
        "#008000", #green
    ]

def __plot_baseline(ax, resource, attribute):
    data = __load_baseline(resource)

    xdata = __get_times_to_plot(data)
    ydata = __get_data_to_plot(data, attribute)

    ax.plot(xdata, ydata, label="Baseline", color="#A9A9A9")

    xevents = EventCollection(xdata, linelength=0.05)
    yevents = EventCollection(ydata, linelength=0.05)

    ax.add_collection(xevents)
    ax.add_collection(yevents)


def plot_metrics(ax, project_path, test_case, resource, attribute, label, color, dashes=False):
    data = __load_metrics(project_path, test_case, resource)

    xdata = __get_times_to_plot(data)
    ydata = __get_data_to_plot(data, attribute)

    line, = ax.plot(xdata, ydata, label=label, color=color)

    if dashes:
        line.set_dashes([2, 2, 2, 2])


def main():
    args = get_args()
    plot_flood = args.flood
    plot_track = args.track
    input_files = args.input_files
    resource = args.resource
    attribute = args.attribute
    output_file = args.output_file
    #plot_baseline = args.baseline
    s = args.s
    c = args.c
    t = args.t

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    colors = __colors()

    #if plot_baseline:
        #__plot_baseline(ax, resource, attribute)

    for index, input in enumerate(input_files):
        #diff = __get_varying_metric(input, s, c, t)

        if plot_flood:
            plot_metrics(ax, FLOOD_PATH, input, resource, attribute, f"QUIC Flood", "#FFA500")

        if plot_track:
            plot_metrics(ax, TR4CK_PATH, input, resource, attribute, f"QUIC Tr4ck", "#3CB371")


    ax.legend(loc="lower right")

    plt.ylabel(f'{resource} {attribute}', fontsize=16)
    plt.xlabel('time (s)', fontsize=16)

    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)

    if not os.path.exists("test_01"):
        os.makedirs("test_01")

    plt.savefig(f"test_01/{output_file}.pdf")
    #plt.show()

if __name__=="__main__":
    main()
