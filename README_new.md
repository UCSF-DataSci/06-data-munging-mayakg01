# Data Cleaning: Population by Group Dataset
## 1. Initial State Data Analysis
### Dataset Overview
-**name**: messy_population_data.csv
-**rows**: 125718
-**columns**: 5

### Column Details of Messy Dataset
| Column Name    | Data Type | Non-Null Count | Unique Values |  Mean |
|----------------|-----------|----------------|---------------|--------  |
| income_groups  | object    |  119412        |    8          | NaN      |
| age            | float     |  119495.00     |   NaN         | 50.007038|
| gender         | float     |  119811.00     |   NaN         | 1.578578 |
| year           | float     |  119516.00     |   NaN         | 2025.068 |
| population     | float     |  1.193780e+05  |   NaN         | 1.112983e+08|

### Identified Issues

1. **[Missing Values]**
    - Description: missing values present in data_original (messy_population_data.csv)
    - Affected Columns: all
    - Example: line 12 of messy_population_data.csv: "high_income,,3.0,1960.0,8172589.0" has a missing value for age
    - Impact: numeric calculations will not be able to be performed for columns where values missing

2. **[Duplicates]**
    - Description: Some rows in messy_population_data.csv are duplicated
    - Affected Columns: all
    - Example: line 1254: "high_income  11.0 1.0  2025.0  7145753.5" and line 2038: "high_income  13.0  2.0  2025.0  7145753.5" have duplicated values for the population and year columns
    - Impact: This will make all summary statistics for the dataset inaccurate if left uncleaned.
3. **[Outliers]**
    - Description: Some values for population are extreme outliers compared to the typical population values included in this dataset.
    - Affected Columns: [population]
    - Example: row 574: "high_income_typo,1.0,2.0,2069.0,544678200.0" : the population column differs from the typical values by orders of magnitude
    - Impact: Outliers that differ by orders of magnitude will heavily skew summary statistics for the population column.
4. **[Incorrect Datatypes]**
    - Description: The gender column has type float64, even though gender is a categorical variable. The year column also has type float64, even though all years are integers.
    - Affected Columns: [year], [gender]
    - Example: line 5: "high_income,0.0,1.0,1953.0,7722053.0" : years and genders are recorded as the float type
    - Impact: Having columns with the correct data type will allow us to perform analyses of the dataset more specifically (ie: only for columns with specified types)
5. **[Inconsistent Categories]**
    - Description: The gender column has option for category "3" as well as 1 and 2, the gender variable should only be able to be recorded as one of two values. Some values in the income_groups column have a "_typo" in their value.
    - Affected Columns: [income_groups], [gender]
    - Example: line 51: "high_income_typo,0.0,1.0,1999.0,6606375.0" : the value in income_groups has a typo
    - Impact: Some income_group rows will not have a valid value and this will affect counts and summary statistics of the dataset. The gender variable counts/statistics will not be able to be interpreted if these invalid categories are left uncleaned. 
6. **[Dates in Future]**
    - Description: Many values in the year column are in the future, ie: after 2024.
    - Affected Columns: [year]
    - Example: line 141: "high_income,0.0,1.0,2089.0,5649436.0" : the year 2089 has not happened yet
    - Impact: The dataset will not be reliable if the accurate years are not documented, future years cannot be included.

## 2. Data Cleaning

### Issue 1: Missing Values

- **Cleaning Method**: For the numeric columns: age, year, population; the missing values were the filled with the median value for that column. For the non-numeric columns: gender, income group: the missing values were filled with the most common value or the mode.
- **Implementation**: 
```python
col_numeric = data_original.select_dtypes(include=[np.number]).columns
data_original[col_numeric] = data_original[col_numeric].fillna(data_original[col_numeric].median())
data_original.dropna(subset=['gender'], inplace=True)
data_original.dropna(subset=['income_groups'], inplace=True)
```
- **Justification**: For numeric variables, as the dataset is very large, using the median value in place is a resonable way to estimate the missing values and not skew summary results. For categorical variables, the missing values are dropped. Filling missing values with a placeholder value or most common value may provide inaccurate associations between variables.
- **Impact**: 
    - Rows affected: 30,978
    - Data distribution change: Shape changed from (125718, 5) to (119412,5) as rows with missing values in categorical columns were dropped.

### Issue 2: Duplicates
- **Cleaning Method**: Duplicates were dropped in place using the drop_duplicates() function
- **Implementation**:
```python
data_original.drop_duplicates(inplace=True)
```
- **Justification**: Duplicates should be removed from the dataset, they will overrpresent certain values and cause inaccurate results.
- **Impact**: 
    - Rows affected: 2789
    - Data distribution change: The shape changed from (119412, 5)to (116623, 5)

### Issue 3: Outliers
- **Cleaning Method**: I found the 25th and 75th percentile values and calculated the IQR range to calculate the lower and upper bounds for non-outlier values. I excluded values above/below these bounds from the cleaned dataset.
- **Implementation**: 
```python
Q1 = data_original['population'].quantile(0.25)
Q3 = data_original['population'].quantile(0.75)
IQR = Q3 - Q1
value_lower = Q1 - 1.5 * IQR
value_upper = Q3 + 1.5 * IQR
data_original = data_original[(data_original['population'] >= value_lower) & (data_original['population'] <= value_upper)]
```
- **Justification**: I used the definition of an outlier to determine the reasonable range for the numeric values and excluded values that did not fall within this range.
- **Impact**: 
    - Rows Affected: 3582
    - Data distribution change: The shape changed from (116623, 5) to (113223, 5)

### Issue 4: Incorrect Datatypes
- **Cleaning Method**: Used the as.type() function to convert columns to the correct data type
- **Implementation**:
```python
data_original['gender'] = data_original['gender'].astype(str)
data_original['year'] = data_original['year'].astype(int)
```
- **Justification**: I used the as.type() function to coerce the columns into the most correct data types: str or object for gender and integer for year.
- **Impact**: 
    - Rows affected: all
    - Data distribution change: no change

### Issue 5: Inconsistent Categories
- **Cleaning Method**: Using the replace() function to remove inconsistent category names
- **Implementation**: 
```python
data_original = data_original[data_original['gender'] != '3.0']
data_original['income_groups'] = data_original['income_groups'].str.replace('_typo', '')
```
- **Justification**: The inconsistent category names: income group names that end in "_typo" and rows that contain gender recorded as "3.0" are being removed so that the dataset will only contain valid category names.
- **Impact**: 
    - Rows Affected: gender: 5795; income_groups: 5489
    - Data distribution change: Shape changes from (113223,5) to (107428, 5)

### Issue 6: Dates in the Future
- **Cleaning Method**: Used the max() to determine the highest future year present, set the max possible year to 2024
- **Implementation**:
```python
year_max = data_original['year'].max()
year_max = 2024
data_original = data_original[(data_original['year'] <= year_max)]
```
- **Justification**: Indexed to select the columns with only present years, not beyond 2024.
- **Impact**:
    - Rows Affected: 62,537
    - Data distribution change: The spread reduced significantly and the shape was changed from (107428, 5) to (50997, 5)

### 3. Final State Analysis
### Dataset Overview
- **name**: cleaned_population_data.csv
- **rows**: 50997
- **columns**: 5

### Column Details
| Column Name   | Data Type | Non-Null Count | #Unique Values |  Mean  |
|---------------|-----------|----------------|----------------|--------|
|[income_groups]| [object]  | [50997]        | [4]            | [NaN]  |
| [age]         | [float]   | [50997]        | [NaN]          | 50.3597 |
| [gender]      | [object]  | [50997]        | [2]            | [NaN]  |
| [year]        | [int]     | [50997]        | [NaN]          |1986.842|
| [population]  | [float]   | [50997]        | [NaN]          |6.258013e+06|

### Summary of Changes
- missing values filled in (numeric) and removed (categorical)
- duplicates and outlier values removed
- inconsistencies in gender and income columns removed
- data types in gender and year coerced to appropriate data types
- future years removed
- the spread in the dataset was reduced signficantly
