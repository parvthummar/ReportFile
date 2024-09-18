import pandas as pd
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator,BayesianEstimator
from pgmpy.inference import VariableElimination

# Define the column headers based on your dataset description
import pandas as pd

# Function to clean and extract diagnosis labels
def clean_diagnosis(diagnosis_str):
    # Remove the record ID and split the diagnosis part
    diagnosis = diagnosis_str.split('[')[0].strip()
    if diagnosis == '-':
        return 'Ne'  # Replace '-' with 'None'
    return diagnosis
def clean_record_id(record_id_str):
    # Remove the leading '-[' and trailing ']' characters
    if pd.isna(record_id_str):
        return None
    cleaned_id = record_id_str.strip(' -[]')
    return cleaned_id
# Load the .data file into a DataFrame
# Assuming the data is comma-separated
data_file = 'thyroid0387.data'  # Replace with the path to your data file
df = pd.read_csv(data_file, delimiter=',', header=None)

# Assign column names based on the attributes you described
columns = [
    'age', 'sex', 'on thyroxine', 'query on thyroxine', 'on antithyroid medication',
    'sick', 'pregnant', 'thyroid surgery', 'I131 treatment', 'query hypothyroid',
    'query hyperthyroid', 'lithium', 'goitre', 'tumor', 'hypopituitary',
    'psych', 'TSH measured', 'TSH', 'T3 measured', 'T3', 'TT4 measured',
    'TT4', 'T4U measured', 'T4U', 'FTI measured', 'FTI', 'TBG measured',
    'TBG', 'referral source', 'diagnosis'
]

# Ensure the DataFrame has the correct number of columns
if len(df.columns) != len(columns):
    raise ValueError(f"Expected {len(columns)} columns, but found {len(df.columns)} columns.")

df.columns = columns

# Process the 'diagnosis' column
df['diagnosis'] = df['diagnosis'].apply(clean_diagnosis)
df['diagnosis'] = df['diagnosis'].apply(clean_record_id)
# Drop the 'record ID' column
#df = df.drop(columns=['record ID'])

# Print the cleaned DataFrame
print(df.head())

# Optionally, save the cleaned DataFrame to a new CSV file
df.to_csv('cleaned_thyroid_data.csv', index=False)

# Define the structure
model = BayesianNetwork([
    ('age', 'diagnosis'),
    ('sex', 'diagnosis'),
    ('TSH', 'diagnosis'),
    ('T3', 'diagnosis'),

])
    # ('on thyroxine', 'TSH'),
    # ('on thyroxine', 'diagnosis'),
    # ('I131 treatment', 'diagnosis')

# Fit the model using Maximum Likelihood Estimation
model.fit(df[["age","sex","TSH","T3","diagnosis"]], estimator=BayesianEstimator)

infer = VariableElimination(model)

# Predict diagnosis for a new patient (provide evidence for features like age, TSH, etc.)
result = infer.map_query(variables=['diagnosis'], evidence={'age': 45, 'TSH': 2.3, 'T3': 1.5, 'sex':'F'})
print(result)
