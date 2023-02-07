import matplotlib.pyplot as plt
import numpy as np
import os
import argparse
import pandas as pd

# pegar os nomes de todos arquivos de log dentro de uma pasta
# ler todos os valores dentro do arquivo de log (do caso de teste)
#

def get_args():
    parser = argparse.ArgumentParser()
    #parser.add_argument("-f", "--flood", action="store_true")
    #parser.add_argument("-k", "--track", action="store_true")
    parser.add_argument("-i", "--input-folder", type=str, nargs="+")
    parser.add_argument("-l", "--labels", type=str, nargs="+")
    parser.add_argument("-o", "--output-file", type=str, default="output-file")
    parser.add_argument("-d", "--output-dir", type=str, default=os.getcwd())
    parser.add_argument("-c", "--cases", type=int, default=3)
    return parser.parse_args()


def get_files(input_folder_path):
    return [f for f in os.listdir(input_folder_path) if os.path.isfile(os.path.join(input_folder_path, f))]


def read_value_from_file(input_folder, filename):
    with open(os.path.join(os.getcwd(), input_folder, filename)) as f:
        return f.readlines()


def fill(arr, obj_len):
    for _ in range(len(arr), obj_len):
        arr.append(arr[1])
    return arr


def get_average(values):
    average = 0.0

    for val in values:
        average += float(val)

    return average/len(values)


def main():
    print("ok, tamo na main")
    args = get_args()
    #plot_flood = args.flood
    #plot_track = args.track
    input_folders = args.input_folder
    labels = args.labels
    output_file = args.output_file
    output_dir = args.output_dir
    num_cases = args.cases

    data = []

    for idx, folder in enumerate(input_folders):
        files_names = get_files(folder)

        group_values = []
        group_values.append(labels[idx])

        for file in files_names:
            values = read_value_from_file(folder, file)
            avg = get_average(values)
            group_values.append(avg)

        if len(group_values) < num_cases:
            print(folder)
            group_values = fill(group_values, num_cases+1)

        data.append(group_values)
        print(group_values)


    input_folders.insert(0, "Requisições por Burst")

    df = pd.DataFrame(data, columns=input_folders)

    ax = df.plot(
        x="Requisições por Burst",
        kind="bar",
        stacked=False,

    )

    ax.set_ylabel("Time (s)")
    plt.legend(loc="lower right")

    plt.show()
    plt.savefig(f"{output_dir}/{output_file}.pdf")

if __name__ == "__main__":
    main()
