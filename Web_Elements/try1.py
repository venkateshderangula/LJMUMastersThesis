import pandas as pd
import os
from collections import defaultdict

# Configuration
DECAY_FACTOR = 0.2  # Recent changes have more impact
MIN_VERSIONS = 3    # Minimum versions required for analysis

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
    LOCATOR_TYPES = [
        'locator_class', 'locator_css', 'locator_id',
        'locator_linkText', 'locator_name', 'locator_partialLinkText',
        'locator_tag', 'locator_xpath', 'text'
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

def calculate_stability_metrics(element_history):
    """Calculate stability metrics for each locator type"""
    stability = defaultdict(lambda: {
        'total_elements': 0,
        'total_changes': 0,
        'recent_changes': 0
    })

    for elem_id, data in element_history.items():
        if data['count'] < MIN_VERSIONS:
            continue

        for locator, history in data['locators'].items():
            if len(history) < MIN_VERSIONS:
                continue

            stability[locator]['total_elements'] += 1
            changes = count_changes(history)
            stability[locator]['total_changes'] += changes
            stability[locator]['recent_changes'] += recent_changes(history)

    return stability

def count_changes(history):
    """Count number of value changes"""
    changes = 0
    prev_value = None
    for version, value in sorted(history, key=lambda x: x[0]):
        if value != prev_value and prev_value is not None:
            changes += 1
        prev_value = value
    return changes

def recent_changes(history):
    """Count changes in last 25% of versions with decay"""
    sorted_history = sorted(history, key=lambda x: x[0])
    recent_cutoff = sorted_history[-int(len(history)*0.25)][0]

    changes = 0
    prev_value = None
    for version, value in sorted_history:
        if version < recent_cutoff:
            continue
        if value != prev_value and prev_value is not None:
            changes += DECAY_FACTOR ** (sorted_history[-1][0] - version)
        prev_value = value
    return changes

def calculate_final_weights(stability_metrics):
    """Calculate normalized weights based on stability"""
    weights = {}
    total_score = 0

    for locator, metrics in stability_metrics.items():
        if metrics['total_elements'] == 0:
            continue

        # Base stability score
        stability = 1 - (metrics['total_changes'] / metrics['total_elements'])

        # Recent change penalty
        recent_penalty = metrics['recent_changes'] / metrics['total_elements']
        adjusted_score = stability * (1 - recent_penalty)

        weights[locator] = adjusted_score
        total_score += adjusted_score

    # Normalize weights
    return {locator: score/total_score for locator, score in weights.items()}

# Usage
if __name__ == "__main__":

    directory_path = "/Users/hnt/Desktop/test_code/next_step/final_1"
    all_apps = next(os.walk(directory_path))[1]
    print(all_apps)

    #calculate weights of attributes for each application
    for app in all_apps:
        directory_path = f"{app}_elements"
        locator_weights = analyze_locator_stability(directory_path)

        print("Optimal Locator Weights:")
        for locator, weight in sorted(locator_weights.items(), key=lambda x: x[1], reverse=True):
            print(f"{locator.ljust(15)}: {weight:.2%}")
