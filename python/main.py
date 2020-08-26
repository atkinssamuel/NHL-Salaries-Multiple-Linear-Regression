from python.consts import *
import numpy as np

def get_feature_index(columns, feature_name):
    return np.where(columns.flatten() == feature_name)[0][0]



if __name__ == "__main__":
    columns = np.load(paths.position_separated + "columns.npy")
    centermen_data = np.load(paths.position_separated + "centermen.npy")
    winger_data = np.load(paths.position_separated + "wingers.npy")
    defensemen_data = np.load(paths.position_separated + "defensemen.npy")

    print("Center-men data shape = {}".format(centermen_data.shape))
    print("Winger data shape = {}".format(winger_data.shape))
    print("Defensemen data shape = {}".format(defensemen_data.shape))
    print("Total data entries = {}".format(sum([centermen_data.shape[0], winger_data.shape[0], defensemen_data.shape[0]])))

