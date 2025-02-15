import pandas as pd
import os
from collections import defaultdict

# Configuration
DECAY_RATE = 0.3  # λ from research
WINDOW_SIZE = 10    # Number of recent versions to consider
BASE_WEIGHTS = {
    'locator_id': 0.4,
    'locator_xpath': 0.3,
    'text': 0.2,
    'locator_css': 0.1
}

def load_versions(directory, num_versions=100):
    """Load all version CSV files into a structured format"""
    elements = defaultdict(lambda: defaultdict(list))

    for version in range(1, num_versions+1):
        file_path = os.path.join(directory, f'version_{version}.csv')
        if not os.path.exists(file_path):
            continue

        df = pd.read_csv(file_path)
        for _, row in df.iterrows():
            widget_id = row['widget_id']
            elements[widget_id]['versions'].append(version)

            # Track presence of each locator type
            for locator in BASE_WEIGHTS.keys():
                has_locator = not pd.isna(row[locator]) and str(row[locator]).strip() != '0'
                elements[widget_id][locator].append(has_locator)

    return elements

def calculate_weights(elements):
    """Calculate recency-weighted scores for all elements"""
    results = {}

    for widget_id, data in elements.items():
        locator_scores = {}
        num_versions = len(data['versions'])

        for locator, presence_list in data.items():
            if locator == 'versions':
                continue

            # Calculate failures in recent versions
            recent_failures = sum(1 for p in presence_list[-WINDOW_SIZE:] if not p)

            # Apply exponential decay
            adjusted_weight = BASE_WEIGHTS[locator] * (1 - DECAY_RATE) ** recent_failures
            locator_scores[locator] = adjusted_weight

        # Store results
        results[widget_id] = {
            'best_locator': max(locator_scores, key=locator_scores.get),
            'scores': locator_scores,
            'total_versions': num_versions,
            'recent_failures': {k: sum(1 for p in v[-WINDOW_SIZE:] if not p)
                              for k, v in data.items() if k != 'versions'}
        }

    return results

def main():
    # Load data from directory containing version CSVs
    data_directory = 'aliexpress_elements/'
    elements_data = load_versions(data_directory)

    # Calculate weights and best locators
    results = calculate_weights(elements_data)

    # Display results
    for widget_id, stats in results.items():
        print(f"\nElement {widget_id} (seen in {stats['total_versions']} versions):")
        print("Recent failures:")
        for locator, failures in stats['recent_failures'].items():
            print(f"  {locator}: {failures} failures")
        print("Adjusted weights:")
        for locator, score in stats['scores'].items():
            print(f"  {locator}: {score:.2f}")
        print(f"Recommended locator: {stats['best_locator']}")

if __name__ == "__main__":
    main()
