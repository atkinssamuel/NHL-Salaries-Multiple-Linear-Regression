from python.consts import *
import numpy as np

def high_level_properties(data, columns):
    print("Columns:", columns)
    print("Number of columns = {}".format(columns.shape[1]))
    print("Number of data entries = {}".format(data.shape[0]))



if __name__ == "__main__":
    data = np.load(paths.concatenated + "data.npy")
    columns = np.load(paths.concatenated + "columns.npy")
    high_level_properties(data, columns)
