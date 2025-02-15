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

    version_files = sorted([f for f in os.listdir(directory) if f.startswith('version_')],
                          key=lambda x: int(x.split('_')[1].split('.')[0]))

    for version_file in version_files:
        version_num = int(version_file.split('_')[1].split('.')[0])
        file_path = os.path.join(directory, version_file)
        df = pd.read_csv(file_path)

        for _, row in df.iterrows():
            widget_id = row['widget_id']
            elements[widget_id]['versions'].append(version_num)

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
        failure_records = {}

        # First pass: collect failures and calculate impacts
        for locator, history in data['locators'].items():
            # Extract failure versions
            failures = [version for version, present in history if not present]
            failure_records[locator] = failures

            # Calculate decayed impact
            decayed_impact = sum(DECAY_RATE ** (max_version - v) for v in failures)

            # Calculate adjusted weight
            base_weight = BASE_WEIGHTS[locator]
            adjusted_weight = base_weight * math.exp(-DECAY_RATE * decayed_impact)
            locator_weights[locator] = adjusted_weight

        # Normalize weights
        total_weight = sum(locator_weights.values())
        normalized_weights = {loc: w/total_weight for loc, w in locator_weights.items()} if total_weight > 0 else locator_weights

        # Store results
        results[widget_id] = {
            'weights': normalized_weights,
            'total_failures': {loc: len(fails) for loc, fails in failure_records.items()},
            'decayed_impact': {loc: sum(DECAY_RATE ** (max_version - v) for v in fails)
                             for loc, fails in failure_records.items()},
            'versions_observed': len(data['versions']),
            'max_version': max_version
        }

    return results

def main():
    data_directory = 'adobe_elements'
    elements_data = load_versions(data_directory)
    results = calculate_historical_weights(elements_data)

    for widget_id, stats in results.items():
        print(f"\nElement {widget_id} (versions: {stats['versions_observed']}, max v{stats['max_version']}):")
        print("Total Failures | Decayed Impact | Final Weight")
        for locator in BASE_WEIGHTS:
            print(f"{locator.ljust(12)}: {stats['total_failures'][locator]:3d} | "
                  f"{stats['decayed_impact'][locator]:7.2f} | {stats['weights'][locator]:6.4f}")
        best = max(stats['weights'], key=stats['weights'].get)
        print(f"Recommended locator: {best}")

if __name__ == "__main__":
    main()
