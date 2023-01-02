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
    parser.add_argument("-o", "--output-file", type=str, default="output-file")
    parser.add_argument("-d", "--output-directory", type=str, default="output-folder")
    parser.add_argument("-y", "--ylim", type=float, nargs='+', default=None)
    parser.add_argument("-x", "--xlim", type=float, nargs='+', default=None)
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

    if label == "vms":
        first_value = int(data[0][label])

        for item in data:
            arr.append(int(item[label]) - first_value)
    else:
        for item in data:
            arr.append(item[label])

    return arr


def __get_times_to_plot(data):
    first = datetime.datetime.strptime(data[0]["timestamp"], '%Y-%m-%d %H:%M:%S.%f')
    last = datetime.datetime.strptime(data[-1]["timestamp"], '%Y-%m-%d %H:%M:%S.%f')
    diff = (last - first).total_seconds()

    arr = np.linspace(0, diff, len(data))
    return arr


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


def plot_metrics(ax, project_path, test_case, resource, attribute, label, dashes=False):
    data = __load_metrics(project_path, test_case, resource)

    xdata = __get_times_to_plot(data)
    ydata = __get_data_to_plot(data, attribute)

    line, = ax.plot(xdata, ydata, label=label)

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
    output_directory = args.output_directory
    xlim = args.xlim
    ylim = args.ylim

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    for index, input in enumerate(input_files):
        if plot_flood:
            plot_metrics(ax, FLOOD_PATH, input, resource, attribute, f"QUIC Flood")

        if plot_track:
            plot_metrics(ax, TR4CK_PATH, input, resource, attribute, f"QUIC Tr4ck")

    if xlim is not None:
        ax.set_xlim(xlim)

    if ylim is not None:
        ax.set_ylim(ylim)

    ax.legend(loc="lower right")

    plt.ylabel(f'{resource} {attribute}', fontsize=16)
    plt.xlabel('time (s)', fontsize=16)

    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)

    plt.tight_layout()

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    plt.savefig(f"{output_directory}/{output_file}.pdf")
    #plt.show()

if __name__=="__main__":
    main()
