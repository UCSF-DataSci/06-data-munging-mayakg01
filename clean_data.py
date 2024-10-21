import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


#Exploratory data analysis
data_original = pd.read_csv('messy_population_data.csv')
print(data_original.describe())
print(data_original.info())

#Details by column 
column_names = data_original.columns
print(column_names)

###Issue 1: Missing Values
print("Missing values in data_original:")
print(data_original.isnull().sum())
print("Initial data shape:", data_original.shape)
#numeric missing values filled with median value for that column
col_numeric = data_original.select_dtypes(include=[np.number]).columns
data_original[col_numeric] = data_original[col_numeric].fillna(data_original[col_numeric].median())
#categorical missing values dropped
data_original.dropna(subset=['gender'], inplace=True)
data_original.dropna(subset=['income_groups'], inplace=True)

print("Missing values after cleaning:")
print(data_original.isnull().sum())
print("Data shape after:", data_original.shape)


#Issue 2: Duplicates
print("Duplicates:", data_original.duplicated().sum())
print("Shape including duplicates:", data_original.shape)

data_original.drop_duplicates(inplace=True)
print("Duplicates after cleaning:", data_original.duplicated().sum())
print("Shape with no duplicates included:", data_original.shape)

data_original.duplicated()
##Issue 3: Outliers
#find the IQR to determine the lower/upper bounds for population values
print("Distribution including outlier values:", data_original.shape)
Q1 = data_original['population'].quantile(0.25)
Q3 = data_original['population'].quantile(0.75)
IQR = Q3 - Q1
value_lower = Q1 - 1.5 * IQR
value_upper = Q3 + 1.5 * IQR
data_original = data_original[(data_original['population'] >= value_lower) & (data_original['population'] <= value_upper)]
print("Distribution with no outliers:", data_original.shape)

#Issue 4: Incorrect Data Types
print("Data Types in original:")
print(data_original.dtypes)

data_original['gender'] = data_original['gender'].astype(str)
data_original['year'] = data_original['year'].astype(int)
print("Data types after cleaning:")
print(data_original.dtypes)

#Issue 5: Inconsistent categories
print("Shape before:", data_original.shape)
print("Categories before:")
print(data_original['gender'].value_counts())
data_original = data_original[data_original['gender'] != '3.0']
print("Categories after cleaning:")
print(data_original['gender'].value_counts())


print("Categories before:")
print(data_original['income_groups'].value_counts())
data_original['income_groups'] = data_original['income_groups'].str.replace('_typo', '')
print("Categories after cleaning:")
print(data_original['income_groups'].value_counts())
print("Shape after:", data_original.shape)

#Issue 6: Years in the Future
year_max = data_original['year'].max()
print("Shape before:", data_original.shape)
print("Highest year before:")
print(year_max)
year_max = 2024
data_original = data_original[(data_original['year'] <= year_max)]
print("Highest year after:")
print(year_max)
print("Shape after:", data_original.shape)

#Summary statistics of dataset after cleaning
print(data_original.describe())
unique_pop = data_original['population'].nunique()
print(unique_pop)
unique_age = data_original['age'].nunique()
print(unique_age)
unique_year = data_original['age'].nunique()
print(unique_year)

#Saving cleaned dataset
data_original.to_csv('cleaned_population_data.csv', index=False)
print("cleaned dataset saved to 'cleaned_population_data.csv'")


