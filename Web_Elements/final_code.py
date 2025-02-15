import pandas as pd
import os
import math
from collections import defaultdict

# Configuration
DECAY_RATE = 0.3  # λ from research
BASE_WEIGHTS = {
    'locator_id': 0.4,
    'locator_xpath': 0.3,
    'text': 0.2,
    'locator_css': 0.1
}

def load_versions(directory):
    """Load all version CSV files into a structured format"""
    elements = defaultdict(lambda: {
        'versions': [],
        'locators': defaultdict(list)
    })

    # First pass: collect all versions and their numbers
    version_files = sorted([f for f in os.listdir(directory) if f.startswith('version_')],
                          key=lambda x: int(x.split('_')[1].split('.')[0]))

    for version_file in version_files:
        version_num = int(version_file.split('_')[1].split('.')[0])
        file_path = os.path.join(directory, version_file)
        df = pd.read_csv(file_path)

        for _, row in df.iterrows():
            widget_id = row['widget_id']
            elements[widget_id]['versions'].append(version_num)

            # Track presence of each locator type in this version
            for locator in BASE_WEIGHTS.keys():
                has_locator = not pd.isna(row[locator]) and str(row[locator]).strip() != '0'
                elements[widget_id]['locators'][locator].append(
                    (version_num, has_locator)
                )

    return elements

def calculate_historical_weights(elements):
    """Calculate weights using full historical data with exponential decay"""
    results = {}

    for widget_id, data in elements.items():
        if not data['versions']:
            continue

        max_version = max(data['versions'])
        locator_weights = {}

        for locator, history in data['locators'].items():
            base_weight = BASE_WEIGHTS[locator]
            failures = [version for version, present in history if not present]

            # Calculate decayed failure impact
            total_decayed_impact = sum(
                DECAY_RATE ** (max_version - version)
                for version in failures
            )

            # Apply exponential decay to base weight
            adjusted_weight = base_weight * math.exp(-DECAY_RATE * total_decayed_impact)
            locator_weights[locator] = adjusted_weight

        # Normalize weights to sum to 1
        total_weight = sum(locator_weights.values())
        if total_weight > 0:
            normalized_weights = {
                locator: weight / total_weight
                for locator, weight in locator_weights.items()
            }
        else:
            normalized_weights = locator_weights

        results[widget_id] = {
            'weights': normalized_weights,
            'total_failures': {locator: len(fails) for locator, fails in data['locators'].items()},
            'decayed_impact': {locator: sum(DECAY_RATE ** (max_version - v) for v in fails)
                             for locator, fails in data['locators'].items()},
            'versions_observed': len(data['versions']),
            'max_version': max_version
        }

    return results

def main():
    # Load data from directory containing version CSVs
    data_directory = 'aliexpress_elements/'
    elements_data = load_versions(data_directory)

    # Calculate historical weights
    results = calculate_historical_weights(elements_data)

    # Display results
    for widget_id, stats in results.items():
        print(f"\nElement {widget_id} (seen in {stats['versions_observed']} versions, up to v{stats['max_version']}):")
        print("Total failures per locator:")
        for locator, fails in stats['total_failures'].items():
            print(f"  {locator}: {fails} failures")
        print("Decayed failure impact:")
        for locator, impact in stats['decayed_impact'].items():
            print(f"  {locator}: {impact:.2f}")
        print("Final weights:")
        for locator, weight in stats['weights'].items():
            print(f"  {locator}: {weight:.4f}")
        best_locator = max(stats['weights'], key=stats['weights'].get)
        print(f"Recommended locator: {best_locator}")

if __name__ == "__main__":
    main()
