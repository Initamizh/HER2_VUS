import os
import json
import pandas as pd
import ast

# Step 1: Load JSON data and convert to DataFrame
json_file_path = "P04626.json"  # Replace with the actual path to your JSON file
with open(json_file_path, "r") as file:
    data = json.load(file)

# Extract the base name without extension
base_name = os.path.splitext(os.path.basename(json_file_path))[0]

# Create the final CSV file name
final_csv_path = f"{base_name}.csv"

# Rest of the script remains unchanged...

# Step 2: Convert to DataFrame
variants = data.get("features", [])
variants_df = pd.DataFrame(variants)

# Save as initial CSV
initial_csv_path = final_csv_path
variants_df.to_csv(initial_csv_path, index=False)
print(f"Variants data saved to {initial_csv_path}")

# Step 3: Load the initial CSV file
df = pd.read_csv(initial_csv_path)

# Define helper functions for parsing each column

# Function to parse 'xrefs' column
def parse_xrefs(xrefs):
    try:
        xrefs_list = ast.literal_eval(xrefs)
    except (ValueError, SyntaxError):
        return pd.Series({'name': '', 'id': '', 'url': '', 'alternativeUrl': ''})
    return pd.Series({
        'name': xrefs_list[0].get('name', ''),
        'id': xrefs_list[0].get('id', ''),
        'url': xrefs_list[0].get('url', ''),
        'alternativeUrl': xrefs_list[0].get('alternativeUrl', '')
    })

# Function to parse 'predictions' column
def parse_predictions(predictions):
    if pd.isna(predictions) or predictions == '':
        return pd.Series({'PredictionValType': '', 'predictorType': '', 'score': '', 'predAlgorithmNameType': '', 'sources': ''})
    try:
        predictions_list = ast.literal_eval(predictions)
    except (ValueError, SyntaxError):
        return pd.Series({'PredictionValType': '', 'predictorType': '', 'score': '', 'predAlgorithmNameType': '', 'sources': ''})
    return pd.Series({
        'PredictionValType': predictions_list[0].get('predictionValType', ''),
        'predictorType': predictions_list[0].get('predictorType', ''),
        'score': predictions_list[0].get('score', ''),
        'predAlgorithmNameType': predictions_list[0].get('predAlgorithmNameType', ''),
        'sources': ', '.join(predictions_list[0].get('sources', []))
    })

# Function to parse 'locations' column
def parse_locations(locations):
    if pd.isna(locations) or locations == '':
        return pd.Series({'loc': '', 'seqId': '', 'source': ''})
    try:
        locations_list = ast.literal_eval(locations)
    except (ValueError, SyntaxError):
        return pd.Series({'loc': '', 'seqId': '', 'source': ''})
    return pd.Series({
        'loc': locations_list[0].get('loc', ''),
        'seqId': locations_list[0].get('seqId', ''),
        'source': locations_list[0].get('source', '')
    })

# Function to parse 'clinicalSignificances' column
def parse_clinical_significances(clinical_significances):
    if pd.isna(clinical_significances) or clinical_significances == '':
        return pd.Series({'type': '', 'sources': '', 'reviewStatus': ''})
    try:
        clinical_significances_list = ast.literal_eval(clinical_significances)
    except (ValueError, SyntaxError):
        return pd.Series({'type': '', 'sources': '', 'reviewStatus': ''})
    return pd.Series({
        'type': clinical_significances_list[0].get('type', ''),
        'sources': ', '.join(clinical_significances_list[0].get('sources', [])),
        'reviewStatus': clinical_significances_list[0].get('reviewStatus', '')
    })

# Function to parse 'populationFrequencies' column
def parse_population_frequencies(population_frequencies):
    if pd.isna(population_frequencies) or population_frequencies == '':
        return pd.Series({'populationName': '', 'frequency': '', 'source': ''})
    try:
        population_frequencies_list = ast.literal_eval(population_frequencies)
    except (ValueError, SyntaxError):
        return pd.Series({'populationName': '', 'frequency': '', 'source': ''})
    return pd.Series({
        'populationName': population_frequencies_list[0].get('populationName', ''),
        'frequency': population_frequencies_list[0].get('frequency', ''),
        'source': population_frequencies_list[0].get('source', '')
    })

# Step 4: Apply parsing functions to respective columns
df[['name', 'id', 'url', 'alternativeUrl']] = df['xrefs'].apply(parse_xrefs)
df[['PredictionValType', 'predictorType', 'score', 'predAlgorithmNameType', 'sources']] = df['predictions'].apply(parse_predictions)
df[['loc', 'seqId', 'source']] = df['locations'].apply(parse_locations)
df[['type', 'sources', 'reviewStatus']] = df['clinicalSignificances'].apply(parse_clinical_significances)
df[['populationName', 'frequency', 'source']] = df['populationFrequencies'].apply(parse_population_frequencies)

# Step 5: Drop original complex columns if not needed
df = df.drop(columns=['xrefs', 'predictions', 'locations', 'clinicalSignificances', 'populationFrequencies'], errors='ignore')

# Step 6: Save the fully parsed DataFrame to the dynamically named CSV
df.to_csv(final_csv_path, index=False)
print(f"Parsed data saved to {final_csv_path}")

# Optionally, print the result to check
print(df.head())