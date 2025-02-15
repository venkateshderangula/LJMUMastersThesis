import pandas as pd
import os
from collections import defaultdict

# Configuration
DECAY_FACTOR = 0.2  # Recent changes have more impact
MIN_VERSIONS = 3     # Minimum versions required for analysis

def analyze_locator_stability(directory):
    """Main analysis function"""
    # Load and preprocess data
    version_data = load_version_data(directory)
    
    # Calculate stability metrics
    stability_metrics = calculate_stability_metrics(version_data)
    
    # Calculate final weights
    weights = calculate_final_weights(stability_metrics)
    
    return weights

def load_version_data(directory):
    """Load and validate version data"""
    versions = sorted([
        f for f in os.listdir(directory) 
        if f.startswith('version_') and f.endswith('.csv')
    ], key=lambda x: int(x.split('_')[1].split('.')[0]))
    
    element_history = defaultdict(lambda: {
        'count': 0,
        'locators': defaultdict(list)
    })
    
    # Updated list of locators to include all specified attributes
    LOCATOR_TYPES = [
        'height', 'locator_class', 'locator_css', 'locator_id',
        'locator_linkText', 'locator_name', 'locator_partialLinkText',
        'locator_tag', 'locator_xpath', 'tag', 'text', 'widget_id',
        'width', 'x', 'y'
    ]
    
    for version_file in versions:
        version_num = int(version_file.split('_')[1].split('.')[0])
        df = pd.read_csv(os.path.join(directory, version_file))
        
        for _, row in df.iterrows():
            elem_id = row['widget_id']
            element_history[elem_id]['count'] += 1
            
            # Record locator values for all specified types
            for locator in LOCATOR_TYPES:
                value = str(row[locator]).strip() if pd.notna(row[locator]) else None
                element_history[elem_id]['locators'][locator].append(
                    (version_num, value)
                )
    
    return element_history

# ... (keep the rest of the functions unchanged from original code)

# Usage
if __name__ == "__main__":
    app =  input("Enter App name: ")
    directory_path = f"{app}_elements"
    locator_weights = analyze_locator_stability(directory_path)
    
    print("Optimal Locator Weights:")
    for locator, weight in sorted(locator_weights.items(), key=lambda x: x[1], reverse=True):
        print(f"{locator.ljust(25)}: {weight:.2%}")
