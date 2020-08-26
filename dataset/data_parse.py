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
raw_columns = train_columns.reshape((1, -1))
raw_data = np.vstack((test_data, train_data))

# The above data includes rookies
# Luckily, a rookie-free version of the dataset was obtained (https://github.com/bradklassen/Predicting_NHL_Salaries/blob/master/NHL_Salaries_ELC_Removed.csv)
# This version of the dataset will be imported and used for the analysis:
with open(paths.rookies_removed + "rookies_removed.csv", errors="ignore") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    data = []
    for row in csv_reader:
        if line_count == 0:
            columns = row
            line_count += 1
        else:
            if str(row[0]) != "":
                data.append(row)
                line_count += 1
    columns = np.array(columns)
    data = np.array(data)

columns = columns.reshape(1, -1)

# Saving concatenated data as .npy save files
np.save(paths.concatenated + "columns", columns)
np.save(paths.concatenated + "data", data)


desired_columns = {"Salary", "Born", "City", "Pr/St", "Cntry", "Nat", "Ht", "Wt", "DftYr", "DftRd", "Ovrl", "Hand", "Last Name", "First Name", "Position", "Team", "GP", "G", "A", "A1", "A2", "PTS", "+/-", "PIM", "Shifts", "TOI", "TOIX", "TOI/GP", "TOI%", "iBLK", "iFOW", "iFOL", "FO%", "OTG", "GWG", "G.Bkhd", "G.Dflct", "G.Slap", "G.Snap", "G.Tip", "G.Wrap",
  "G.Wrst", "CBar", "Post", "Over", "Wide", "S.Bkhd", "S.Dflct", "S.Slap",
  "S.Snap", "S.Tip", "S.Wrap", "S.Wrst"}

desired_indices = []
added_set = set()
for i in range(len(columns[0])):
    if columns[0][i] in desired_columns:
        if columns[0][i] not in added_set:
            desired_indices.append(i)
            added_set.add(columns[0][i])

updated_columns = columns[0][desired_indices]

data = data[:, desired_indices]
columns = columns[:, desired_indices]

position_index = np.where(updated_columns == "Position")


centermen = "C"
left_wingers = "LW"
right_wingers = "RW"
defensemen = "D"

centermen_data = []
winger_data = []
defensemen_data = []

for i in range(data.shape[0]):
    if data[i][14][0] == centermen:
        centermen_data.append(data[i])
    elif data[i][14][0] == defensemen:
        defensemen_data.append(data[i])
    else:
        winger_data.append(data[i])

centermen_data = np.array(centermen_data)
winger_data = np.array(winger_data)
defensemen_data = np.array(defensemen_data)

print("Center-men data shape = {}".format(centermen_data.shape))
print("Winger data shape = {}".format(winger_data.shape))
print("Defensemen data shape = {}".format(defensemen_data.shape))
print("Total data entries = {}".format(sum([centermen_data.shape[0], winger_data.shape[0], defensemen_data.shape[0]])))

# Saving position separated data:
np.save(paths.position_separated + "columns", columns)
np.save(paths.position_separated + "centermen", centermen_data)
np.save(paths.position_separated + "wingers", winger_data)
np.save(paths.position_separated + "defensemen", defensemen_data)
