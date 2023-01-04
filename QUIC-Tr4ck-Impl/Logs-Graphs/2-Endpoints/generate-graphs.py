import json
import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
import datetime
import numpy as np
import argparse
import random
import os

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
    abs_path = os.getcwd()
    with open(f"{abs_path}/{project_path}/{test_case}/server-{resource}.json", "r") as json_file:
        full_logs = "[" + json_file.read()[:-2] + "]"
        return (json.loads(full_logs))


def __get_data_to_plot(data, label):
    arr = []

    if label == "vms":
        first_value = float(data[0][label])

        for item in data:
            value = round((float(item[label]) - first_value)/(1024 * 1024))
            arr.append(value)
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


def get_y_label(resource, attribute):
    if attribute == "vms":
        return f"Virtual Memory Size (MB)"
    else:
        return f"% {resource.capitalize()}"


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
            plot_metrics(ax, f"QUIC-flood", input, resource, attribute, f"QUIC Flood")

        if plot_track:
            plot_metrics(ax, f"QUIC-Tr4ck", input, resource, attribute, f"QUIC Tr4ck")

    if xlim is not None:
        ax.set_xlim(xlim)

    if ylim is not None:
        ax.set_ylim(ylim)

    ax.legend(loc="lower right")

    plt.ylabel(get_y_label(resource, attribute), fontsize=16)
    plt.xlabel('Time (s)', fontsize=16)

    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)

    plt.tight_layout()

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    plt.savefig(f"{output_directory}/{output_file}.pdf")
    #plt.show()

if __name__=="__main__":
    main()
