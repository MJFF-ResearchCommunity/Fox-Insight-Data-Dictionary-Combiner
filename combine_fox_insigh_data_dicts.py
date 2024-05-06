# function to combine the Fox Insight data dictionaries into a single DataFrame
# The function reads the two CSV files, creates a dictionary of variable values for each variable, merges the value_description dictionary with the df_variable DataFrame, and selects the required columns to form the final DataFrame.
# Change the path to the two dictionary fies as needed

import pandas as pd
import numpy as np

df_variable=pd.read_csv('FoxInsightVariables.csv')
df_value=pd.read_csv('FoxInsightValues.csv')

# Sort dictionary by keys
def sort_dict_by_keys(d):
    if not isinstance(d, dict):
        return {}
    # Ensure keys are strings for comparison and sorting
    sorted_keys = sorted(d.keys(), key=lambda x: (not isinstance(x, str), str(x)))
    return {k: d[k] for k in sorted_keys}


# Create a dictionary of variable values for each variable
value_description_dict = df_value.groupby('variable').apply(lambda x: dict(zip(x['value'], x['value_description']))).to_dict()
# Merge the value_description dictionary with the df_variable DataFrame
df_variable['value_dict'] = df_variable['variable'].map(value_description_dict)
# Apply the function to the 'value_dict' column
df_variable['value_dict'] = df_variable['value_dict'].apply(sort_dict_by_keys)

# Selecting the required columns to form the final DataFrame
final_df = df_variable[['category', 'variable', 'value_dict',  'variable_description',]]
final_df.to_csv('FoxInsightDataDictionary.csv', index=False)