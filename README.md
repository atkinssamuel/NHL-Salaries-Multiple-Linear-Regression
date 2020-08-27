# NHL-Salaries-Multiple-Linear-Regression
This repository includes a multiple linear regression analysis of the salaries of NHL players. A complete preliminary analysis of the dataset was conducted and the details of this analysis are included in the [dataset section](https://github.com/atkinssamuel/NHL-Salaries-Multiple-Linear-Regression/tree/master/dataset). This section also includes a key for the meaning of each of the dataset features and a link to the source of the dataset.

## Features
The features that remained after removing duplicate columns and columns that did not have an apparent impact on each player's salary are as follows:

*NOTE: These are not the raw abbreviated versions of these features. Columns that had a tremendous amount of faulty or empty cells were also removed (DrftYr, DrftRd, Ovrl).*


```Salary, Born, City, Province/State, Country, Nationality, Height, Weight, Handedness, Last Name, First Name, Position, Team, Games Played, Goals, Assists, First Assists, Second Assists, Points, +/-, PIM, Shifts, TOI, TOI/GP, TOI%, Blocked Shots, Face-offs Won, Face-offs Lost, Face-off Percentage, Overtime Goals, Game-Winning Goals, Backhand Goals, Deflection Goals, Slap-Shot Goals, Snapshot Goals, Tip Goals, Wrap Around Goals, Crossbars Hit, Posts Hit, Shots Over the Net, Shots Wide of the Net, Backhand Shots, Deflected Shots, Slap-Shots, Snapshots, Tipped Shots, Wrap-Around Shots, Wrist-Shots```


Prior to hypothesizing which features may be linearly correlated with salary, we must first segregate players according to their position. This must be done because center-men, wingers, and defense-men are all compensated uniquely. 

After organizing the dataset according to each player's position, we must now remove the rookie players. This is a necessary step because rookies are required to adhere to entry-level contracts. These contracts pay significantly less than normal contracts and will undoubtedly skew the data. 

Now that the data has been parsed for potential skew factors, potential linear correlations will now be noted for each position. Note that there may be correlations between features that were not included and unexpected correlations between certain features and the salary. 

A player should hypothetically be paid according to the value that he brings to the team. The term value, in this context, should be defined as the number of wins a team achieves each year. To win games, teams must score more goals than their opponents. Therefore, a player's value can be measured by how successfully he generates goals for his team, and how successfully he prevents the enemy team from scoring. Center-men, wingers, and defense-men all provide value for their teams in unique ways. 

A center-man generates value for his team by primarily generating scoring opportunities for his team. He can generate these opportunities by winning face-offs, scoring goals, and assisting goals. A center-man's value also depends on his ability to shut down the enemy team. As such, we expect his value to also depend on his +/-, the number of shots he has blocked, and other defensive statistics. 
 
 ![](images/face-off.jpg)

We expect a winger's salary to depend on the same elements that a center-man's salary depends on with one major exception: face-offs. Given that wingers rarely take face-offs, their value likely is not dependent on the number of face-offs that they win or lose. Furthermore, the number of goals that wingers score on average is different than the number of goals center-men score. This will impact the weight value attached to the number of goals a player scores. 

![](images/one-timer.jpg)

Unlike the forwards, a defense-man's value depends much more on his defensive contributions. Although some of a defense-man's value may depend on his offensive contributions, the weighting of this value is undoubtedly different. As such, a separate analysis must be conducted for defense-man. Note that the TOIX and TOI% features had to be ignored for defense-men because of the staggering amount of empty cells.

![](images/blocked-shot.jpg)

----------------------

## Checking for Linear Relationships
Center-men, wingers, and defensemen were all considered individually. Scatter plots between each potential independent variable and salary were created for each positional dataset. Clear linear relationships were noted. Furthermore, the r-value (Pearson product-moment correlation) and the p-value was also computed for each independent-dependent variable pair. 

The Pearson product-moment correlation is the ratio of the covariance of a set of data pairs and the product of the two standard deviations of those data pairs. The covariance of two random variables, x and y, is as follows:

![](images/equations/covariance.png)

The standard deviation of a random variable x, is:

![](images/equations/standard-deviation.png)

Therefore, the product of the standard deviations of two random variables, x and y, is:

![](images/equations/std-deviation-product.png)

The ratio, then, of the covariance of a set of data pairs and the product of their standard deviations is:

![](images/equations/r-value.png)

An r-value that approaches +1 indicates a strong positive correlation, an r-value that approaches -1 indicates a strong negative correlation, and an r value that does not approach -1 or +1 does not indicate a linear relationship between the data pairs. Variable pairs that possessed an r-value less than -0.6 or greater than 0.6 were considered. 
 
The p-value was also computed for each feature. The p-value is the probability that we would have observed the data given that the null hypothesis is true. In this context the null hypothesis is that the data is not linearly correlated. Therefore, the p-value in this context is the probability that we would have observed the data if the correlation coefficients were zero (the data is not linearly correlated). The p-value is determined by first finding the t-value. 

![](images/equations/t-value.png)

This value allows us to observe the 2-tailed p-value by consulting a t-distribution table.

After determining which variables are correlated with the dependent variable, salary, we must then check for multi-collinearity. Multi-collinearity occurs when two independent variables are linearly correlated. When this occurs, the two variables are redundant and one of them should be excluded. We will determine if two independent variables are correlated using the same techniques we used for the dependent-independent data pairs. 

After determining which variables are linearly correlated with the output variable, we can conduct our multi-linear regression analysis. 

## MLR Analysis
Since we are assuming that the dependent variable is linearly correlated with the dependent variables, the equation that describes the relationship between the salary, y, and the data features, x<sub>1</sub> to x<sub>k</sub> is:

![](images/equations/least-squares-eqn.png)

The epsilon in the above is the residual of the regression equation and the beta values

![](images/equations/beta.png)

are the ideal weights. Since we do not know the ideal weights, we must formulate an estimate based on our observations (data). An individual observation, y<sub>i</sub>, can be written as follows:

![](images/equations/y-i.png)

If we have a total of n observations we can express the n equations associated with the n observations in matrix form:

![](images/equations/matrix-form-eqn.png)

If we assign the following variables:

![](images/equations/capital_y.png)
![](images/equations/capital_x.png)
![](images/equations/capital_beta.png)
![](images/equations/capital-epsilon.png)

Our equation in matrix form becomes:

![](images/equations/y-x-b-e.png)

Rearranging for the residual (error):

![](images/equations/epsilon-equation.png)

We wish to minimize the least squared error. To do this, we will first express the least squared error in simple terms:

![](images/equations/MLR-deriv-1.png)

Then, we will take the derivative of the least squared error:

![](images/equations/MLR-deriv-2.png)

And finally, to minimize the least squared error, we will set the derivative to equal 0:

![](images/equations/MLR-deriv-3.png)

As shown above, we now have an estimate for the ideal weights in the context of multi-linear regression. We can use this estimate to create a model that accurately describes the relationship between the independent variables and the dependent output variable. 



