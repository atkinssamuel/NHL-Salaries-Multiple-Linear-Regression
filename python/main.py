from python.consts import *
import numpy as np
import matplotlib.pyplot as plt

def get_feature_index(columns, feature_name):
    return np.where(columns.flatten() == feature_name)[0][0]

def get_feature_indices(columns, features):
    feature_indices = []
    for i in range(len(features)):
        feature_indices.append(get_feature_index(columns, features[i]))
    return np.array(feature_indices)

def get_feature_from_index(columns, feature_index):
    return columns[feature_index]

def get_data_column(data, feature_index):
    data_column = data[:, feature_index].flatten()
    data_column[np.where(data_column == "")] = -1
    return np.array(data_column, dtype=float)

# def compute_pearson_correlation_coefficient(x, y):


def independent_dependent_correlation_testing(data, columns, testing_features):
    salary_data = get_data_column(data, get_feature_index(columns, "Salary"))
    for testing_feature in testing_features:
        print("Testing Feature = {}".format(testing_feature))
        testing_feature_index = get_feature_index(columns, testing_feature)
        testing_feature_data = get_data_column(data, testing_feature_index)

        # r_value = compute_pearson_correlation_coefficient(salary_data, testing_feature_data)
        plt.scatter(testing_feature_data, salary_data)
        plt.show()

if __name__ == "__main__":
    columns = np.load(paths.position_separated + "columns.npy")
    centermen_data = np.load(paths.position_separated + "centermen.npy")
    winger_data = np.load(paths.position_separated + "wingers.npy")
    defensemen_data = np.load(paths.position_separated + "defensemen.npy")

    print("Center-men data shape = {}".format(centermen_data.shape))
    print("Winger data shape = {}".format(winger_data.shape))
    print("Defensemen data shape = {}".format(defensemen_data.shape))
    print("Total data entries = {}".format(sum([centermen_data.shape[0], winger_data.shape[0], defensemen_data.shape[0]])))

    salary_index = get_feature_index(columns, "Salary")
    testing_features = ['Ht', 'Wt', 'DftYr', 'DftRd', 'Ovrl', 'GP', 'G', 'A', 'A1', 'A2', 'PTS', '+/-', 'PIM', 'Shifts', 'TOI', 'TOIX', 'TOI/GP', 'TOI%', 'iBLK', 'iFOW', 'iFOL', 'FO%', 'OTG', 'GWG', 'G.Bkhd', 'G.Dflct', 'G.Slap', 'G.Snap', 'G.Tip', 'G.Wrap', 'G.Wrst', 'Post', 'Over', 'Wide', 'S.Bkhd', 'S.Dflct', 'S.Slap', 'S.Snap', 'S.Tip', 'S.Wrap', 'S.Wrst']

    testing_feature_indices = get_feature_indices(columns, testing_features)

    independent_dependent_correlation_testing(centermen_data, columns, testing_features)

