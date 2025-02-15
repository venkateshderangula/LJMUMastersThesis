import os
import glob
import math
import pandas as pd
import numpy as np

# -------------------------------
# Step 1: Load All CSV Files and Add a Version Column
# -------------------------------

# Folder containing your CSV files (e.g., "version1.csv", "version2.csv", …)
folder_path = "aliexpress_widget_csv"  # Adjust if necessary

# Look for files with names like "version*.csv"
csv_files = glob.glob(os.path.join(folder_path, "version*.csv"))
if not csv_files:
    raise ValueError("No CSV files found in the folder. Please check the folder path and file naming.")

dfs = []
for file in csv_files:
    base = os.path.basename(file)
    try:
        # Expecting filenames like "version1.csv" (extract the number)
        version_str = base.split("_")[1].split(".")[0]
        version_num = int(version_str)
    except Exception as e:
        print(f"Could not extract version from {base}: {e}")
        continue
    df = pd.read_csv(file)
    df["version"] = version_num
    dfs.append(df)

# Combine all DataFrames into one
all_data = pd.concat(dfs, ignore_index=True)
print(f"Loaded data from {all_data['version'].nunique()} versions, total {len(all_data)} records.")

# -------------------------------
# Step 2: Create a Signature for Each Widget
# -------------------------------

# Adjust the column names as needed.
# We assume your CSV files include these columns: tag, locator_id, locator_name, text.
def create_signature(row):
    tag = str(row.get("tag", "")).lower().strip()
    locator_id = str(row.get("locator_id", "")).strip()
    # Treat "0" as missing.
    if locator_id == "0":
        locator_id = ""
    locator_name = str(row.get("locator_name", "")).strip()
    if locator_name == "0":
        locator_name = ""
    text = str(row.get("text", "")).lower().strip()
    # Join the parts with a delimiter.
    signature = "||".join([tag, locator_id, locator_name, text])
    return signature

all_data["signature"] = all_data.apply(create_signature, axis=1)

# -------------------------------
# Step 3: Define Locator Columns to Analyze
# -------------------------------

locator_columns = [
    "locator_id",
    "locator_name",
    "locator_class",
    "locator_linkText",
    "locator_partialLinkText",
    "locator_xpath",
    "locator_css"
]

# For consistency, convert all locator values to lowercase strings and treat "0" as empty.
for col in locator_columns:
    all_data[col] = all_data[col].astype(str).apply(lambda x: "" if x.strip() == "0" else x.strip().lower())

# -------------------------------
# Step 4: Group Widgets by Signature and Compute Stability for Each Locator Type
# -------------------------------

grouped = all_data.groupby("signature")

# We'll store stability scores for each locator type in a dictionary.
stability_scores = {col: [] for col in locator_columns}

# For each widget cluster (group)...
for sig, group in grouped:
    for col in locator_columns:
        # Get the non-empty values for this locator type.
        values = group[col].dropna().astype(str).str.strip()
        values = values[values != ""]
        if len(values) == 0:
            stability = 0.0
        else:
            # Count frequency of each distinct value.
            counts = values.value_counts()
            # Stability is the frequency of the most common value divided by the total count.
            stability = counts.iloc[0] / len(values)
        stability_scores[col].append(stability)

# Compute the average stability for each locator type across all clusters.
avg_stability = {col: np.mean(stability_scores[col]) for col, scores in stability_scores.items()}

print("\nAverage Stability for Each Locator Type:")
for col, score in avg_stability.items():
    print(f"{col}: {score:.3f}")

# -------------------------------
# (Optional) Save Detailed Cluster Stability Data for Further Analysis
# -------------------------------
cluster_stability = []
for sig, group in grouped:
    cluster_data = {"signature": sig, "cluster_size": len(group)}
    for col in locator_columns:
        values = group[col].dropna().astype(str).str.strip()
        values = values[values != ""]
        if len(values) == 0:
            cluster_data[col + "_stability"] = 0.0
        else:
            counts = values.value_counts()
            cluster_data[col + "_stability"] = counts.iloc[0] / len(values)
    cluster_stability.append(cluster_data)

clusters_df = pd.DataFrame(cluster_stability)
clusters_df.to_csv("clusters_stability1.csv", index=False)
print("\nDetailed cluster stability data saved to clusters_stability.csv")
