import pandas as pd
from collections import defaultdict

# Load the CSV file
df = pd.read_csv('normalized_locator_weights.csv')

# Initialize a nested dictionary to store the results
output = defaultdict(lambda: {"locators": {}})

# Process each row in the DataFrame
for _, row in df.iterrows():
    app = row['Application']
    locator = row['Attribute']
    weight = round(row['Normalized'], 3)  # Round to 3 decimal places

    # Add to the nested dictionary
    output[app]['locators'][locator] = weight

# Convert defaultdict to a regular dictionary for final output
output = {app: data for app, data in output.items()}

# Print the result (or save as JSON)
import json
print(json.dumps(output, indent=4))

# Save the JSON output to a file
with open('output_weights_final.json', 'w') as f:
    json.dump(output, f, indent=4)

print("JSON data has been saved to output.json")
