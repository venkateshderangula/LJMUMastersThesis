import pandas as pd
import os
from collections import defaultdict
import time
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
        file_path = os.path.join(directory, version_file)

        try:
            # Attempt to read the CSV file
            df = pd.read_csv(file_path)

            # Check if the file is empty
            if df.empty:
                print(f"Warning: File {version_file} is empty. Skipping.")
                continue

            for _, row in df.iterrows():
                elem_id = row['widget_id']
                element_history[elem_id]['count'] += 1

                # Record locator values for all specified types
                for locator in LOCATOR_TYPES:
                    value = str(row[locator]).strip() if pd.notna(row[locator]) else None
                    element_history[elem_id]['locators'][locator].append(
                        (version_num, value)
                    )

        except pd.errors.EmptyDataError:
            print(f"Warning: File {version_file} is empty or malformed. Skipping.")
            continue
        except KeyError as e:
            print(f"Warning: Missing required column in {version_file}. Error: {e}. Skipping.")
            continue
        except Exception as e:
            print(f"Warning: Error reading {version_file}. Error: {e}. Skipping.")
            continue
    return element_history

def save_all_weights_to_file(all_weights, output_file):
    """Save weights from multiple applications to a single CSV file"""
    # Combine all weights into a single DataFrame
    combined_data = []

    for app_name, weights in all_weights.items():
        for attribute, weight in weights.items():
            combined_data.append({
                'Application': app_name,
                'Attribute': attribute,
                'Weight': weight
            })

    # Create DataFrame and save to CSV
    weights_df = pd.DataFrame(combined_data)
    weights_df.to_csv(output_file, index=False)
    print(f"\nAll weights saved to {output_file}")


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
    start = time.process_time()


    base_path = "/Users/hnt/Desktop/test_code/next_step/final_1"
    all_apps = next(os.walk(base_path))[1]
    print(all_apps)

    #calculate weights of attributes for each application
    output_file = "all_applications_weights.csv"  # Output file for all applications
    all_weights = {}

    # Run analysis for each application
    for app_name in all_apps:
        print(f"\nAnalyzing {app_name}...")
        # directory_path =  f"{app_name}"
        locator_weights = analyze_locator_stability(app_name)
        all_weights[app_name] = locator_weights

        # Print results for this application
        print(f"\nOptimal Locator Weights for {app_name}:")
        for locator, weight in sorted(locator_weights.items(), key=lambda x: x[1], reverse=True):
            print(f"{locator.ljust(25)}: {weight:.2%}")

    # Time taken by the alogrithm to calculate the weights. 
    print(time.process_time() - start)
    # Save all weights to a single file
    save_all_weights_to_file(all_weights, output_file)
