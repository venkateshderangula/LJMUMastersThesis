import json

# Load the JSON file
with open('output_weights_final.json', 'r') as f:
    data = json.load(f)

# Count the number of applications (top-level keys)
num_applications = len(data)
print(f"Number of applications: {num_applications}")
