import pandas as pd
import os
import math
from collections import defaultdict

# Configuration
DECAY_RATE = 0.3
BASE_WEIGHTS = {
    'locator_id': 0.4,
    'locator_xpath': 0.3,
    'text': 0.2,
    'locator_css': 0.1
}

def load_versions(directory):
    """Load versions with element persistence validation"""
    elements = defaultdict(lambda: {
        'versions': [],
        'locators': defaultdict(list)
    })

    version_files = sorted([f for f in os.listdir(directory) if f.startswith('version_')],
                          key=lambda x: int(x.split('_')[1].split('.')[0]))

    # First pass: collect all widget IDs across versions
    all_widget_ids = set()
    for version_file in version_files:
        file_path = os.path.join(directory, version_file)
        df = pd.read_csv(file_path)
        all_widget_ids.update(df['widget_id'].unique())

    # Second pass: verify persistent elements
    persistent_elements = {}
    for widget_id in all_widget_ids:
        persistent = True
        for version_file in version_files:
            file_path = os.path.join(directory, version_file)
            df = pd.read_csv(file_path)
            if widget_id not in df['widget_id'].values:
                persistent = False
                break
        if persistent:
            persistent_elements[widget_id] = True

    # Third pass: load only persistent elements
    for version_file in version_files:
        version_num = int(version_file.split('_')[1].split('.')[0])
        file_path = os.path.join(directory, version_file)
        df = pd.read_csv(file_path)

        # Filter for persistent elements
        df = df[df['widget_id'].isin(persistent_elements)]

        for _, row in df.iterrows():
            widget_id = row['widget_id']

            for locator in BASE_WEIGHTS.keys():
                has_locator = not pd.isna(row[locator]) and str(row[locator]).strip() not in ['0', '']
                elements[widget_id]['locators'][locator].append(
                    (version_num, has_locator)
                )
            elements[widget_id]['versions'].append(version_num)

    return elements

def calculate_historical_weights(elements):
    """Enhanced weight calculation with element persistence check"""
    results = {}

    for widget_id, data in elements.items():
        if len(data['versions']) < 2:  # Skip elements with <2 versions
            continue

        max_version = max(data['versions'])
        locator_weights = {}
        failure_records = {}

        for locator, history in data['locators'].items():
            failures = [v for v, present in history if not present]
            failure_records[locator] = failures

            decayed_impact = sum(DECAY_RATE ** (max_version - v) for v in failures)
            base_weight = BASE_WEIGHTS[locator]
            adjusted_weight = base_weight * math.exp(-DECAY_RATE * decayed_impact)
            locator_weights[locator] = adjusted_weight

        total_weight = sum(locator_weights.values())
        normalized_weights = {loc: w/total_weight for loc, w in locator_weights.items()} if total_weight > 0 else locator_weights

        results[widget_id] = {
            'weights': normalized_weights,
            'total_failures': {loc: len(fails) for loc, fails in failure_records.items()},
            'decayed_impact': {loc: sum(DECAY_RATE ** (max_version - v) for v in fails)
                             for loc, fails in failure_records.items()},
            'versions_observed': len(data['versions']),
            'version_range': f"{min(data['versions'])}-{max_version}"
        }

    return results

def main():
    data_directory = 'adobe_elements'
    elements_data = load_versions(data_directory)
    results = calculate_historical_weights(elements_data)

    if not results:
        print("No elements with version history found!")
        print("Verify widget IDs persist across versions in your CSVs")
        return

    for widget_id, stats in results.items():
        for locator in BASE_WEIGHTS:
            print(f"{locator.ljust(12)} | {stats['total_failures'][locator]:7d} | {stats['decayed_impact'][locator]:14.2f} | {stats['weights'][locator]:6.4f}")
        best = max(stats['weights'], key=stats['weights'].get)
        print(f"Recommended locator: {best} (confidence: {stats['weights'][best]:.2%})")

if __name__ == "__main__":
    main()
