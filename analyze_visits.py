import pandas as pd
import numpy as np
import random

# Part I: Load and structure the data
df = pd.read_csv('ms_data.csv') # read in csv
df['visit_date'] = pd.to_datetime(df['visit_date']) # conver to datetime

df = df.sort_values(by=['patient_id', 'visit_date']) # sort by patient id and visit date

# handling missing data
if df['walking_speed'].isnull().any(): # if walking speed is null
        df['walking_speed'] = df['walking_speed'].fillna(df['walking_speed'].mean()) # fill with mean

# Remove rows with missing patient_id or visit_date
df = df.dropna(subset=['patient_id', 'visit_date'])

# Part II: Add insurance information
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
base = np.random.randint(100, 1000, size=len(df))
    
# subtract discount based on insurance type
df['visit_cost'] = base * (1 - df['insurance_type'].map(discounts))

# Part III: Calculate Summary Statistics

mean_s_by_e = df.groupby('education_level')['walking_speed'].mean() # mean walk speed by edu
print("Mean Walking Speed by education level:")
print(mean_s_by_e)

# Mean costs by insurance type
mean_c_by_i = df.groupby('insurance_type')['visit_cost'].mean() # mean cost by insurance type
print("Mean Cost by Insurance Type:")
print(mean_c_by_i)

# Correlation between age and walking speed
a_s_corr = df['age'].corr(df['walking_speed']) # age effects on walking speed
print("Age Effects on Walking Speed:")
print(a_s_corr)


