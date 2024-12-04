import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.regression.mixed_linear_model import MixedLM
import seaborn as sns
import matplotlib.pyplot as plt
import random
from statsmodels.stats.anova import anova_lm
from scipy.stats import ttest_ind, f_oneway


df = pd.read_csv('ms_data.csv') # read in csv
df['visit_date'] = pd.to_datetime(df['visit_date'])
df = df.sort_values(by=['patient_id', 'visit_date']) # sort by patient id and visit date

# handling missing data
if df['walking_speed'].isnull().any(): # if walking speed is null
        df['walking_speed'] = df['walking_speed'].fillna(df['walking_speed'].mean()) # fill with mean

# Remove rows with missing patient_id or visit_date
df = df.dropna(subset=['patient_id', 'visit_date'])

with open('insurance.lst', 'r') as file:
    insurance_types = file.read().splitlines()[1:]  # skip the header

    patient_ids = df['patient_id'].unique() # only map for each unique patient ID
    insurance_mapping = {pid: random.choice(insurance_types) for pid in patient_ids} # generate random insurance types
    df['insurance_type'] = df['patient_id'].map(insurance_mapping) # map insurance type to patient id

# discounts based on insurance type
discounts = {
    'Basic': 0.0, 
    'Premium': 0.2,
    'Platinum': 0.5
    }

# generate random base between $100 and $1000
random.seed(16)
base = np.random.randint(100, 1000, size=len(df))
    
# subtract discount based on insurance type
df['visit_cost'] = base * (1 - df['insurance_type'].map(discounts))

# part 1: speed walking analysis ---------------------------------------------------------------
model = smf.ols(
    'walking_speed ~ age + education_level',
    data=df
) # regression for walking speed
speed = model.fit()
print("Multiple Regression for Walking Speed:")
print(speed.summary()) # print multiple regression
print()

# check for outliers
Q1 = df['walking_speed'].quantile(0.25) # find Q1 and Q3
Q3 = df['walking_speed'].quantile(0.75)
IQR = Q3 - Q1 # calculate interquartile range

lower_bound = Q1 - 1.5 * IQR # calculate lower and upper bounds
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df['walking_speed'] < lower_bound) | (df['walking_speed'] > upper_bound)] # find outliers

print(f"Outliers Count: {len(outliers)}")
print(outliers) # print outliers
print()

#remove outliers
df = df[(df['walking_speed'] >= lower_bound) & (df['walking_speed'] <= upper_bound)]

# test for significant trends
anova_table = anova_lm(speed, typ=2)
print("Statistical Test Results:")
print(anova_table)
print('//////////////////////////////////////////////////////')

# Part 2: insurance type analysis ---------------------------------------------------------
order = ['Basic', 'Premium', 'Platinum']
sns.boxplot(x='insurance_type', y='visit_cost', data=df, order=order) # create boxplot
plt.title('Visit Costs by Insurance Type') # insert title
plt.xlabel('Insurance Type') # label x-axis
plt.ylabel('Cost of Visit') # label y-axis
plt.savefig('insurance_boxplot.png', dpi=300, bbox_inches='tight') # save figure as a png

cost_stats = df.groupby('insurance_type')['visit_cost'].agg(['mean', 'std']) # aggregate by insurance type
print("Summary Statistics for Visit Costs by Insurance Type:")
print(cost_stats) # print means and standard deviation of visit ocst by insurance type

from scipy.stats import f_oneway

# Subset visit costs by insurance type
basic = df[df['insurance_type'] == 'Basic']['visit_cost']
premium = df[df['insurance_type'] == 'Premium']['visit_cost']
platinum = df[df['insurance_type'] == 'Platinum']['visit_cost']

# Perform ANOVA
anova_result = f_oneway(basic, premium, platinum)
print(f"ANOVA F-statistic: {anova_result.statistic:.2f}, p-value: {anova_result.pvalue:.5f}")
print()


sst = df['visit_cost'].var() * (len(df) - 1) # Calculate total sum of squares (SST) 
ssb = sum(df.groupby('insurance_type')['visit_cost'].size() * 
          (df.groupby('insurance_type')['visit_cost'].mean() - df['visit_cost'].mean())**2) #between-group sum of squares (SSB)

# Calculate eta squared
eta_squared = ssb / sst
print(f"Effect Size: {eta_squared:.2f}")


# Part 3: Advanced analysis ---------------------------------------------------------------
# Create interaction
df['education_age_interaction'] = df['age'] * df['education_level'].map({
    'High School': 0, 
    'Some College': 1, 
    'Bachelors': 2, 
    'Graduate': 3
})

# Formula to control confounders
formula = 'walking_speed ~ age * education_level + insurance_type'

# Fit the model
interaction_model = smf.ols(formula=formula, data=df).fit()

# Summary of results
print("Regression Results with Interaction:")
print(interaction_model.summary())

# Extract key statistics
coefficients = interaction_model.params
pvalues = interaction_model.pvalues
conf_int = interaction_model.conf_int()

print("Key Statistics:")
print(pvalues)
print = (conf_int)



