# Dataset Exploration
The dataset used for this analysis can be found on Kaggle: https://www.kaggle.com/camnugent/predict-nhl-player-salaries. This dataset includes information regarding 874 NHL hockey players during the 2016-2017 regular season.
## Raw Dataset Form
The dataset comes split up into three files: train.csv, test.csv, and test_salaries.csv. The owner of the dataset performed a machine learning analysis of the data which is why the dataset was initially split up like this. Our analysis is linear in nature. Therefore, we do not need a training and testing set. 

The first step of this project was to take the training, testing, and testing inference data and concatenate it. This was accomplished in the ```data_parse.py``` file and the concatenated dataset was stored in the ```dataset/concatenated``` folder as .npy save objects.

## High-Level Dataset Analysis
The dataset has a total of 154 columns and 874 entries. Given the tremendous amount of columns, only apparently important columns were selected for this analysis. Furthermore, many of the columns of the raw data are duplicates. These duplicates were removed. 

Prior to conducting an analysis of possible linear relationships that may exist in the dataset, it is important to investigate what each column means in the context of a player's value As such, the meaning of each selected column is illustrated by the table below:

| Column Abbreviation  | Meaning  | Relevance  |
|:---|:---|:---|
| Salary  | Salary  |  The player's salary in USD |
|  Born | Born  | - |
| City  | City  | - |
| Pr/St |  Province/State | - |
| Cntry | Country | - |
| Nat | Nationality | - |
| Ht | Height | The player's height in inches |
| Wt | Weight | The player's weight in lbs |
| DftYr | Draft Year | - |
| DftRd | Draft Round | - |
| Ovrl | Overall | The player's overall draft pick value |
| Hand | Handedness | -  |
| Last Name | - | - |
| First Name | - | - |
| Position | - | - |
| Team | - | - |
| GP | Games Played  | - |
| G | Goals | - |
| A |  Assists | - |
| A1 | First Assists  | Assists in which the player was the last person to touch the puck before the goal scorer |
| A2 |  Second Assists | Assists in which the player was the second last person to touch the puck before the goal scorer  |
| PTS | Points | - |
| +/- |  Plus/Minus | The number of even strength goals for that the player was on the ice for minus the number of even strength goals against |
| PIM | Penalty Minutes | - |
| Shifts | - | The number of shifts that the player was on for during the entire season |
| TOI | Time On Ice | - |
| TOI/GP | Time On Ice/Games Played | - |
| TOI% | - | The percentage of the game that the player played on average |
| iBLK | Blocked Shots | - |
| iFOW | Face-offs Won | - |
| iFOL | Face-offs Lost | - |
| FO% | Face-off Percentage | - |
| OTG | Overtime Goals | - |
| GWG | Game-Winning Goals | - |
| G.Bkhd | Backhand Goals | - |
| G.Dflct | Deflection Goals | - |
| G.Slap | Slap-Shot Goals | - |
| G.Snap | Snapshot Goals | - |
| G.Tip | Tip Goals | - |
| G.Wrap | Wrap Around Goals | - |
| G.Wrst | Wrist-Shot Goals | - |
| CBar | Crossbars Hit | - |
| Post | Posts Hit | - |
| Over | Shots Over the Net | - |
| Wide | Shots Wide of the Net | - |
| S.Bkhd | Backhand Shots | - |
| S.Dflct | Deflected Shots | - |
| S.Slap | Slap-Shots | - |
| S.Snap | Snapshots | - |
| S.Tip | Tipped Shots | - |
| S.Wrap | Wrap-Around Shots | - |
| S.Wrst | Wrist-Shots | - |

These columns were chosen because they were hypothesized to have some impact on each player's salary. 

## Further Parsing
Given that a rookie player's entry level contract is significantly lower than other players' contracts regardless of their seasonal performance, it may be wise to remove rookies from the analysis. Furthermore, defense-men, wingers, and center-men will all be compensated differently for their statistical performance. It is not expected of a super-star center-man to block hundreds of shots each year. Moreover, an elite defense-man may only tally a handful of points. These differences must be taken into account during the analysis. 