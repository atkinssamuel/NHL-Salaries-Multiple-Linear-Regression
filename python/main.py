from python.consts import *
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from mpl_toolkits.mplot3d import axes3d


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
    mean_x = np.ones((len(x), 1)) * np.mean(x)
    mean_y = np.ones((len(y), 1)) * np.mean(y)
    return (np.matmul(np.transpose(x.reshape(len(x), 1) - mean_x), y.reshape(len(y), 1) - mean_y) / len(x)).flatten()


def compute_pearson_correlation_coefficient(x, y):
    # r-value = covariance(x, y) / std(x) * std(y)
    return covariance(x, y) / (np.std(x) * np.std(y))


def compute_t_value(r, n):
    return r * np.sqrt(n - 2) / np.sqrt(1 - np.power(r, 2))


def compute_p_value(t, n):
    return stats.t.sf(np.abs(t), n - 1) * 2


def compute_weights(X, Y):
    return np.matmul(np.linalg.inv(np.matmul(np.transpose(X), X)), np.matmul(np.transpose(X), Y))


def dv_iv_correlation_test(data, columns, testing_features, dataset_title, dataset_lower, save_dest):
    salary_data = get_data_column(data, get_feature_index(columns, "Salary"))
    correlation_metrics = []
    print("\n{}:".format(dataset_title))
    for testing_feature in testing_features:
        plt.clf()
        print("Testing Feature = {}".format(testing_feature))
        testing_feature_index = get_feature_index(columns, testing_feature)
        testing_feature_data = get_data_column(data, testing_feature_index)
        n = len(testing_feature_data)

        r_value = compute_pearson_correlation_coefficient(testing_feature_data, salary_data)
        p_value = compute_p_value(compute_t_value(r_value, n), n)
        correlation_metrics.append([testing_feature, r_value, p_value])
        salary_data_m = salary_data / 1000000
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

    correlation_headers = np.array(["Test Feature", "R-Value", "P-Value"]).reshape((1, -1))
    return np.vstack((correlation_headers, correlation_metrics))


def dv_dv_correlation_test(data, columns, testing_features, dataset_title, dataset_lower, save_dest):
    correlation_metrics = []
    print("\n{}:".format(dataset_title))
    for i in range(len(testing_features)):
        testing_feature_A = testing_features[i]
        for j in range(len(testing_features)):
            testing_feature_B = testing_features[j]
            plt.clf()
            print("Testing Feature A = {}".format(testing_feature_A))
            print("Testing Feature B = {}".format(testing_feature_B))

            testing_feature_index_A = get_feature_index(columns, testing_feature_A)
            testing_feature_data_A = get_data_column(data, testing_feature_index_A)

            testing_feature_index_B = get_feature_index(columns, testing_feature_B)
            testing_feature_data_B = get_data_column(data, testing_feature_index_B)

            n = len(testing_feature_data_A)

            r_value = compute_pearson_correlation_coefficient(testing_feature_data_A, testing_feature_data_B)
            correlation_metrics.append(
                [testing_feature_A, testing_feature_B, r_value, compute_p_value(compute_t_value(r_value, n), n)])

            plt.scatter(testing_feature_data_A, testing_feature_data_B, s=0.7)
            plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)
            plt.title("{} - {} vs. {}".format(dataset_title, testing_feature_A, testing_feature_B))
            plt.xlabel("{}".format(testing_feature_A))
            plt.ylabel("{}".format(testing_feature_B))

            testing_feature_A_temp = testing_feature_A.replace(".", "_")
            testing_feature_A_temp = testing_feature_A_temp.replace("+/-", "plus_minus")
            testing_feature_A_temp = testing_feature_A_temp.replace("/", "_")

            testing_feature_B_temp = testing_feature_B.replace(".", "_")
            testing_feature_B_temp = testing_feature_B_temp.replace("+/-", "plus_minus")
            testing_feature_B_temp = testing_feature_B_temp.replace("/", "_")

            plt.savefig(save_dest + "{}_{}_vs_{}".format(dataset_lower, testing_feature_A_temp, testing_feature_B_temp))
            plt.close()
            # plt.show()
    correlation_headers = np.array(["Test Feature A", "Test Feature B", "R-Value", "P-Value"]).reshape((1, -1))
    return np.vstack((correlation_headers, correlation_metrics))


if __name__ == "__main__":
    dv_iv_correlation_testing = False
    dv_dv_correlation_testing = False
    MLR_anal = True

    centermen_anal = False
    winger_anal = False
    defensemen_anal = True

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

    if dv_iv_correlation_testing:
        if centermen_anal:
            c_corr_values = dv_iv_correlation_test(centermen_data, columns, \
                                                   testing_features, \
                                                   "Centermen Data", \
                                                   "centermen", \
                                                   paths.centermen_results + paths.dv_iv_scatter)
            c_corr_values = np.asarray(c_corr_values)
            np.savetxt(paths.centermen_results + 'c_corr_values.csv', c_corr_values, delimiter=',', fmt="%s")

        original_testing_features = testing_features
        testing_features.remove("TOIX")
        testing_features.remove("TOI%")

        if defensemen_anal:
            d_corr_values = dv_iv_correlation_test(defensemen_data, columns, \
                                                   testing_features, \
                                                   "Defensemen Data", \
                                                   "defensemen", \
                                                   paths.defensemen_results + paths.dv_iv_scatter)

            d_r_values = np.asarray(d_corr_values)
            np.savetxt(paths.defensemen_results + 'd_corr_values.csv', d_corr_values, delimiter=',', fmt="%s")

        testing_features = original_testing_features
        if winger_anal:
            w_corr_values = dv_iv_correlation_test(centermen_data, columns, \
                                                   testing_features, \
                                                   "Winger Data", \
                                                   "wingers", \
                                                   paths.winger_results + paths.dv_iv_scatter)
            w_corr_values = np.asarray(w_corr_values)
            np.savetxt(paths.winger_results + 'w_corr_values.csv', w_corr_values, delimiter=',', fmt="%s")

    if dv_dv_correlation_testing:
        # These are the variables that are linearly correlated with the output variable for centermen:
        if centermen_anal:
            centermen_testing_features = ['Ht', 'Wt', 'GP', 'G', 'A', 'A1', 'A2', 'PTS', '+/-', 'Shifts', 'TOI', 'TOIX', \
                                          'TOI/GP', 'TOI%', 'iBLK', 'iFOW', 'iFOL', 'FO%', 'OTG', 'GWG', 'G.Bkhd',
                                          'G.Snap', \
                                          'G.Tip', 'G.Wrap', 'G.Wrst', 'Post', 'Over', 'Wide', 'S.Bkhd', 'S.Dflct',
                                          'S.Slap', \
                                          'S.Tip', 'S.Wrap', 'S.Wrst']
            c_dv_dv_matrix = dv_dv_correlation_test(centermen_data, columns, \
                                                    centermen_testing_features, \
                                                    "Centermen Data", \
                                                    "centermen", \
                                                    paths.centermen_results + paths.dv_iv_scatter)
            c_dv_dv_matrix = np.asarray(c_dv_dv_matrix)
            np.savetxt(paths.centermen_results + 'c_dv_dv_matrix.csv', c_dv_dv_matrix, delimiter=',', fmt="%s")

        # These are the variables that are linearly correlated with the output variable for wingers:
        if winger_anal:
            winger_testing_features = ['Ht', 'Wt', 'GP', 'G', 'A', 'A1', 'A2', 'PTS', 'PIM', 'Shifts',
                                       'TOI', 'TOI/GP', 'iBLK', 'iFOW', 'iFOL', 'FO%', 'OTG', 'GWG',
                                       'G.Bkhd',
                                       'G.Slap', 'G.Snap', 'G.Tip', 'G.Wrap', 'G.Wrst', 'Post', 'Over', 'Wide',
                                       'S.Bkhd',
                                       'S.Dflct', 'S.Slap', 'S.Snap', 'S.Tip', 'S.Wrap', 'S.Wrst']
            w_dv_dv_matrix = dv_dv_correlation_test(defensemen_data, columns, \
                                                    winger_testing_features, \
                                                    "Winger Data", \
                                                    "wingers", \
                                                    paths.winger_results + paths.dv_iv_scatter)
            w_dv_dv_matrix = np.asarray(w_dv_dv_matrix)
            np.savetxt(paths.winger_results + 'w_dv_dv_matrix.csv', w_dv_dv_matrix, delimiter=',', fmt="%s")

        # These are the variables that are linearly correlated with the output variable for defensemen:
        if defensemen_anal:
            defensemen_testing_features = ['Wt', 'GP', 'G', 'A', 'A1', 'A2', 'PTS', 'PIM', 'Shifts',
                        'TOI', 'TOI/GP', 'iBLK', 'OTG', 'GWG',
                        'G.Dflct', 'G.Slap', 'G.Snap', 'G.Tip', 'G.Wrst', 'Post', 'Over', 'Wide', 'S.Bkhd',
                        'S.Dflct', 'S.Slap', 'S.Snap', 'S.Tip', 'S.Wrst']
            d_dv_dv_matrix = dv_dv_correlation_test(defensemen_data, columns, \
                                                    defensemen_testing_features, \
                                                    "Defensemen Data", \
                                                    "defensemen", \
                                                    paths.defensemen_results + paths.dv_iv_scatter)
            d_dv_dv_matrix = np.asarray(d_dv_dv_matrix)
            np.savetxt(paths.defensemen_results + 'd_dv_dv_matrix.csv', d_dv_dv_matrix, delimiter=',', fmt="%s")

    if MLR_anal:
        if centermen_anal:
            Y = np.array(centermen_data[:, get_feature_index(columns, "Salary")], dtype=float).reshape(-1, 1)
            ones = np.ones((len(Y), 1))
            X1 = np.array(centermen_data[:, get_feature_index(columns, "A")], dtype=float).reshape(-1, 1)
            X = np.hstack((ones, X1))
            centermen_beta = compute_weights(X, Y)
            print("Beta Associated w/ the Center-men Dataset = {}".format(centermen_beta))

            b0 = 515342.73458342
            b1 = 139618.94964624

            x = np.array([i for i in range(60)]).reshape((60, 1))
            y = np.ones((60, 1)) * b0 + x * b1
            Y = Y / 1000000
            plt.scatter(X1, Y, s=1)
            y = y / 1000000
            plt.plot(x, y, 'g')
            plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)
            plt.title("Center-men Linear Model")
            plt.xlabel("Assists")
            plt.ylabel("Salary $USD (in millions)")
            plt.savefig(paths.centermen_results + "centermen_model")
            plt.show()


        if winger_anal:
            Y = np.array(centermen_data[:, get_feature_index(columns, "Salary")], dtype=float).reshape(-1, 1)
            ones = np.ones((len(Y), 1))
            X1 = np.array(centermen_data[:, get_feature_index(columns, "A")], dtype=float).reshape(-1, 1)
            X2 = np.array(centermen_data[:, get_feature_index(columns, "iFOW")], dtype=float).reshape(-1, 1)
            X = np.hstack((ones, np.hstack((X1, X2))))
            winger_beta = compute_weights(X, Y)
            print("Beta Associated w/ the Winger Dataset = {}".format(winger_beta))

            b0 = 330849.13104956
            b1 = 86156.90770201
            b2 = 3462.39882529

            fig = plt.figure(figsize=(6, 6))
            ax = fig.add_subplot(111, projection='3d')
            Y = Y / 1000000
            ax.scatter3D(X1, X2, Y)

            x1, x2 = np.arange(0, 60, 0.1), np.arange(0, 1000, 0.1)
            x1, x2 = np.meshgrid(x1, x2)
            z = (b0 + x1 * b1 + x2 * b2)/1000000
            ax.plot_surface(x1, x2, z, color="Green")
            plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)
            plt.xlabel("Assists")
            plt.ylabel("Face-offs Won")
            plt.title("Winger Multi-Linear Model")
            ax.set_zlabel("Salary $USD (in millions)")
            plt.savefig(paths.winger_results + "winger_model")
            plt.show()

        if defensemen_anal:
            Y = np.array(centermen_data[:, get_feature_index(columns, "Salary")], dtype=float).reshape(-1, 1)
            ones = np.ones((len(Y), 1))
            X1 = np.array(centermen_data[:, get_feature_index(columns, "TOI/GP")], dtype=float).reshape(-1, 1)
            X2 = np.array(centermen_data[:, get_feature_index(columns, "Wt")], dtype=float).reshape(-1, 1)
            X = np.hstack((ones, np.hstack((X1, X2))))
            defensemen_beta = compute_weights(X, Y)
            print("Beta Associated w/ the Defense-men Dataset = {}".format(defensemen_beta))

            b0 = -8512128.46386528
            b1 = 529646.26848097
            b2 = 18688.71378825

            fig = plt.figure(figsize=(6, 6))
            ax = fig.add_subplot(111, projection='3d')
            Y = Y / 1000000
            ax.scatter3D(X1, X2, Y)

            x1, x2 = np.arange(0, 30, 0.1), np.arange(150, 250, 0.1)
            x1, x2 = np.meshgrid(x1, x2)
            z = (b0 + x1 * b1 + x2 * b2) / 1000000
            ax.plot_surface(x1, x2, z, color="Green")
            plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)
            plt.xlabel("TOI/GP")
            plt.ylabel("Wt")
            plt.title("Defense-men Multi-Linear Model")
            ax.set_zlabel("Salary $USD (in millions)")
            plt.savefig(paths.defensemen_results + "defensemen_model")
            plt.show()

