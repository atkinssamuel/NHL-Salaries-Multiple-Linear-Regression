# NHL-Salaries-Multiple-Linear-Regression
This repository includes a multiple linear regression analysis of the salaries of NHL players. A complete preliminary analysis of the dataset was conducted and the details of this analysis are included in the [dataset section](https://github.com/atkinssamuel/NHL-Salaries-Multiple-Linear-Regression/tree/master/dataset). This section also includes a key for the meaning of each of the dataset features and a link to the source of the dataset.

## Features
The features that remained after removing duplicate columns and columns that did not have an apparent impact on each player's salary are as follows:

*NOTE: These are not the raw abbreviated versions of these features.*


```Salary, Born, City, Province/State, Country, Nationality, Height, Weight, Draft Year, Draft Round, Overall, Handedness, Last Name, First Name, Position, Team, Games Played, Goals, Assists, First Assists, Second Assists, Points, +/-, PIM, Shifts, TOI, TOI/GP, TOI%, Blocked Shots, Face-offs Won, Face-offs Lost, Face-off Percentage, Overtime Goals, Game-Winning Goals, Backhand Goals, Deflection Goals, Slap-Shot Goals, Snapshot Goals, Tip Goals, Wrap Around Goals, Crossbars Hit, Posts Hit, Shots Over the Net, Shots Wide of the Net, Backhand Shots, Deflected Shots, Slap-Shots, Snapshots, Tipped Shots, Wrap-Around Shots, Wrist-Shots```


Prior to hypothesizing which features may be linearly correlated with salary, we must first segregate players according to their position. This must be done because center-men, wingers, and defense-men are all compensated uniquely. 

After organizing the dataset according to each player's position, we must now remove the rookie players. This is a necessary step because rookies are required to adhere to entry-level contracts. These contracts pay significantly less than normal contracts and will undoubtedly skew the data. 

Now that the data has been parsed for potential skew factors, potential linear correlations will now be noted for each position. Note that there may be correlations between features that were not included and unexpected correlations between certain features and the salary. 

A player should hypothetically be paid according to the value that he brings to the team. The term value, in this context, should be defined as the number of wins a team achieves each year. To win games, teams must score more goals than their opponents. Therefore, a player's value can be measured by how successfully he generates goals for his team, and how successfully he prevents the enemy team from scoring. Center-men, wingers, and defense-men all provide value for their teams in unique ways. 

A center-man generates value for his team by primarily generating scoring opportunities for his team. He can generate these opportunities by winning face-offs, scoring goals, and assisting goals. A center-man's value also depends on his ability to shut down the enemy team. As such, we expect his value to also depend on his +/-, the number of shots he has blocked, and other defensive statistics. 
 
 ![](images/face-off.jpg)

We expect a winger's salary to depend on the same elements that a center-man's salary depends on with one major exception: face-offs. Given that wingers rarely take face-offs, their value likely is not dependent on the number of face-offs that they win or lose. Furthermore, the number of goals that wingers score on average is different than the number of goals center-men score. This will impact the weight value attached to the number of goals a player scores. 

![](images/one-timer.jpg)

Unlike the forwards, a defense-man's value depends much more on his defensive contributions. Although some of a defense-man's value may depend on his offensive contributions, the weighting of this value is undoubtedly different. As such, a separate analysis must be conducted for defense-man. 

![](images/blocked-shot.jpg)

----------------------

## Data Analysis
Center-men, wingers, and defensemen were all considered individually. Scatter plots between each potential independent variable and salary were created for each positional dataset. Clear linear relationships were noted. Furthermore, the r-value (Pearson product-moment correlation) and the p-value was also computed for each independent-dependent variable pair. 

The Pearson product-moment correlation is the ratio of the covariance of a set of data pairs and the product of the two standard deviations of those data pairs. An r-value that approaches +1 indicates a strong positive correlation, an r-value that approaches -1 indicates a strong negative correlation, and an r value that does not approach -1 or +1 does not indicate a linear relationship between the data pairs. Variable pairs that possessed an r-value less than -0.6 or greater than 0.6 were considered. 
 
The p-value was also computed for each feature. The p-value is the probability that we would have observed the data given that the null hypothesis is true. In this context the null hypothesis is that the data is not linearly correlated. Therefore, the p-value in this context is the probability that we would have observed the data if the correlation coefficients were zero (the data is not linearly correlated).

