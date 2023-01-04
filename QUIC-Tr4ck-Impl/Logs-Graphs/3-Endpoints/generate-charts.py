import matplotlib.pyplot as plt
import numpy as np
import os

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--flood", action="store_true")
    parser.add_argument("-k", "--track", action="store_true")
    parser.add_argument("-i", "--input-folder", type=str, nargs='+')
    parser.add_argument("-o", "--output-file", type=str, default="output-file")
    parser.add_argument("-d", "--output-directory", type=str, default="output-folder")
    return parser.parse_args()

def get_files(input_folder_path):
    return [f for f in os.listdir(input_folder_path) if os.path.isfile(os.path.join(input_folder_path, f))]

def main():
    
