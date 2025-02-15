import pandas as pd

# Load raw weights data
raw_df = pd.read_csv("all_applications_weights.csv")

def normalize_weights(group):
    """Min-max normalization within each application group"""
    min_w = group['Weight'].min()
    max_w = group['Weight'].max()

    # Handle identical weights case
    if min_w == max_w:
        group['Normalized'] = 0.5
    else:
        group['Normalized'] = (group['Weight'] - min_w) / (max_w - min_w)

    return group

# Apply normalization per application
normalized_df = raw_df.groupby('Application', group_keys=False).apply(normalize_weights)

# Save results
normalized_df.to_csv("normalized_locator_weights.csv", index=False)
