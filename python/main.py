from python.consts import *
import numpy as np
import matplotlib.pyplot as plt
# save to csv file

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
    # print(np.sum(np.where([data_column == ""])))
    return np.array(data_column, dtype=float)


def covariance(x, y):
    mean_x = np.ones((len(x), 1))*np.mean(x)
    mean_y = np.ones((len(y), 1))*np.mean(y)
    return (np.matmul(np.transpose(x.reshape(len(x), 1) - mean_x), y.reshape(len(y), 1) - mean_y)/len(x)).flatten()



def compute_pearson_correlation_coefficient(x, y):
    # r-value = covariance(x, y) / std(x) * std(y)
    return covariance(x, y) / (np.std(x) * np.std(y))


def compute_t_value(r, n):
    return r * np.sqrt(n - 2) / np.sqrt(1 - np.power(r, 2))


def compute_weights(X, Y):
    return np.matmul(np.inv(np.matmul(X, np.transpose(X))), np.matmul(np.transpose(X), Y))


def dv_iv_correlation_test(data, columns, testing_features, dataset_title, dataset_lower, save_dest):
    salary_data = get_data_column(data, get_feature_index(columns, "Salary"))
    r_values = []
    print("\n{}:".format(dataset_title))
    for testing_feature in testing_features:
        plt.clf()
        print("Testing Feature = {}".format(testing_feature))
        testing_feature_index = get_feature_index(columns, testing_feature)
        testing_feature_data = get_data_column(data, testing_feature_index)

        r_value = compute_pearson_correlation_coefficient(testing_feature_data, salary_data)
        r_values.append([testing_feature, r_value])
        salary_data_m = salary_data/1000000
        plt.scatter(testing_feature_data, salary_data_m, s=0.7)
        plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)
        plt.title("{} - Salary vs. {}".format(dataset_title, testing_feature))
        plt.xlabel("{}".format(testing_feature))
        plt.ylabel("Salary $USD (in millions)")

        testing_feature = testing_feature.replace(".", "_")
        testing_feature = testing_feature.replace("+/-", "plus_minus")
        testing_feature = testing_feature.replace("/", "_")

        plt.savefig(save_dest + "{}_{}".format(dataset_lower, testing_feature))
        plt.close()
        # plt.show()
    return r_values

def dv_dv_correlation_test(data, columns, testing_features, dataset_title, dataset_lower, save_dest):
    r_values = np.zeros((len(testing_features), len(testing_features), 3))
    print("\n{}:".format(dataset_title))
    for i in range(len(testing_features)):
        testing_feature_A = testing_features[i]
        for j in range(i, len(testing_features)):
            testing_feature_B = testing_features[j]
            plt.clf()
            print("Testing Feature A = {}".format(testing_feature_A))
            print("Testing Feature B = {}".format(testing_feature_B))

            testing_feature_index_A = get_feature_index(columns, testing_feature_A)
            testing_feature_data_A = get_data_column(data, testing_feature_index_A)

            testing_feature_index_B = get_feature_index(columns, testing_feature_B)
            testing_feature_data_B = get_data_column(data, testing_feature_index_B)

            r_values[i, j] = [testing_feature_A, testing_feature_B, compute_pearson_correlation_coefficient(testing_feature_data_A, testing_feature_data_B)]
            plt.scatter(testing_feature_data_A, testing_feature_data_B, s=0.7)
            plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)
            plt.title("{} - {} vs. {}".format(dataset_title, testing_feature_A, testing_feature_B))
            plt.xlabel("{}".format(testing_feature_A))
            plt.ylabel("{}".format(testing_feature_B))

            testing_feature = testing_feature.replace(".", "_")
            testing_feature = testing_feature.replace("+/-", "plus_minus")
            testing_feature = testing_feature.replace("/", "_")

            plt.savefig(save_dest + "{}_{}_vs_{}".format(dataset_lower, testing_feature_A, testing_feature_B))
            plt.close()
            # plt.show()
    return r_values


if __name__ == "__main__":
    correlation_testing = True

    columns = np.load(paths.position_separated + "columns.npy")
    centermen_data = np.load(paths.position_separated + "centermen.npy")
    winger_data = np.load(paths.position_separated + "wingers.npy")
    defensemen_data = np.load(paths.position_separated + "defensemen.npy")

    print("Center-men data shape = {}".format(centermen_data.shape))
    print("Winger data shape = {}".format(winger_data.shape))
    print("Defensemen data shape = {}".format(defensemen_data.shape))
    print("Total data entries = {}".format(
        sum([centermen_data.shape[0], winger_data.shape[0], defensemen_data.shape[0]])))

    salary_index = get_feature_index(columns, "Salary")
    testing_features = ['Ht', 'Wt', 'GP', 'G', 'A', 'A1', 'A2', 'PTS', '+/-', 'PIM', 'Shifts',
                        'TOI', 'TOIX', 'TOI/GP', 'TOI%', 'iBLK', 'iFOW', 'iFOL', 'FO%', 'OTG', 'GWG', 'G.Bkhd',
                        'G.Dflct', 'G.Slap', 'G.Snap', 'G.Tip', 'G.Wrap', 'G.Wrst', 'Post', 'Over', 'Wide', 'S.Bkhd',
                        'S.Dflct', 'S.Slap', 'S.Snap', 'S.Tip', 'S.Wrap', 'S.Wrst']

    testing_feature_indices = get_feature_indices(columns, testing_features)

    if correlation_testing:
        c_r_values = dv_iv_correlation_test(centermen_data, columns, \
                               testing_features, \
                               "Centermen Data", \
                               "centermen", \
                               paths.centermen_results + paths.dv_iv_scatter)
        c_r_values = np.asarray(c_r_values)
        np.savetxt(paths.centermen_results + 'c_r_values.csv', c_r_values, delimiter=',', fmt="%s")

        original_testing_features = testing_features
        testing_features.remove("TOIX")
        testing_features.remove("TOI%")
        d_r_values = dv_iv_correlation_test(defensemen_data, columns, \
                               testing_features, \
                               "Defensemen Data", \
                               "defensemen", \
                               paths.defensemen_results + paths.dv_iv_scatter)

        d_r_values = np.asarray(d_r_values)
        np.savetxt(paths.defensemen_results + 'd_r_values.csv', d_r_values, delimiter=',', fmt="%s")

        testing_features = original_testing_features
        w_r_values = dv_iv_correlation_test(centermen_data, columns, \
                               testing_features, \
                               "Winger Data", \
                               "wingers", \
                               paths.winger_results + paths.dv_iv_scatter)
        w_r_values = np.asarray(w_r_values)
        np.savetxt(paths.winger_results + 'w_r_values.csv', w_r_values, delimiter=',', fmt="%s")

        c_r_dv_dv_matrix = dv_dv_correlation_test(centermen_data, columns, \
                                            testing_features, \
                                            "Centermen Data", \
                                            "centermen", \
                                            paths.centermen_results + paths.dv_iv_scatter)
        c_r_matrix = np.asarray(c_r_dv_dv_matrix)
        np.savetxt(paths.centermen_results + 'c_r_dv_dv_matrix.csv', c_r_dv_dv_matrix, delimiter=',', fmt="%s")
