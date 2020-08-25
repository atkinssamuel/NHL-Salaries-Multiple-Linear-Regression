import csv
import numpy as np
from python.consts import *


with open(paths.raw + "test.csv", errors="ignore") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    test_data = []
    for row in csv_reader:
        if line_count == 0:
            test_columns = row
            line_count += 1
        else:
             test_data.append(row)
    test_columns = np.array(test_columns)
    test_data = np.array(test_data)

with open(paths.raw + "test_salaries.csv", errors="ignore") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    test_salary_data = []
    for row in csv_reader:
        if line_count == 0:
            test_salary_columns = row
            line_count += 1
        else:
             test_salary_data.append(row)
    test_salary_columns = np.array(test_salary_columns)
    test_salary_data = np.array(test_salary_data)

# Joining test data with the test salary data
test_columns = np.hstack((test_salary_columns, test_columns))
test_data = np.hstack((test_salary_data, test_data))

with open(paths.raw + "train.csv", errors="ignore") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    train_data = []
    for row in csv_reader:
        if line_count == 0:
            train_columns = row
            line_count += 1
        else:
            train_data.append(row)
    train_columns = np.array(train_columns)
    train_data = np.array(train_data)

# Reshaping data appropriately
columns = train_columns.reshape((1, -1))
data = np.vstack((test_data, train_data))

# Saving concatenated data as .npy save files
np.save(paths.concatenated + "columns", columns)
np.save(paths.concatenated + "data", data)
