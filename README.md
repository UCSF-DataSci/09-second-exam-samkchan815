# DATASCI 217 Final Exam
## Samantha Chan

## Question 1: Data Preparation with Command-Line Tools
To clean and prepare the data, I first ran `generate_dirty_data.py` to generate the csv file. 
Using the `grep` and `sed` commands, I removed the empty lines, comments, and extra comments. 
In order to select certain columns for our clean csv file, I used the `cut` command. Next, I 
create the `insurance.lst` file. Using `echo` I listed variables for the new variable. Finally, 
using the `head` command, I printed the first few rows, and the total number of visits.

## Question 2: Data Analysis with Python
In `analyze_visits.py`, I first loaded the csv file and cleaned the data. I then randomly
generated insurance information, using a dictionary to account for price differences in each
insurance type. Finally to find the summary statistics, I used aggregation and output the
information for each.

## Question 3: Statistical Analysis
### Analyze Walking Speed
For the multiple regression for walking speed, the model has an R-squared of 0.801, which indicates that approximately 80.1% of the variance in walking speed is explained by the predictors. We can also see that education level significantly affects walking speed, which is illustrated by the coefficients. High school is associated with a decrease in walking speed by 0.7876, while graduate school is associated with an increase in walking speed by 0.4032. In addition age has a significantly negative coefficient of -0.0302, which indicates that wlaking speed decreases as age increases. Based on the ANOVA results, eduacation level and age are highly significant with a p-value less than 0.05. 

| Variable | Coefficient |
| Graduate School | 0.4032 |
| High School | -0.7876 |
| Some College | -0.3985 |
| Age | -0.0302 |

When running our analysis, we found that there were three outliers. To refine our model, we removed these outliers, making our results more accurate and representative of our population. Overall, yes, education level affects walking speed with graduate school being associated with highest speed and high school associated with lowest speed. Age also influences walking speed because as age increases, walking speed decreases. 