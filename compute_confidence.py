import json
import os
from collections import defaultdict

def load_json_file(filename):
    with open(filename, "r") as file:
        return json.load(file)

def aggregate_confidence(num_files=10):
    confidence_sums = defaultdict(float)
    confidence_counts = defaultdict(int)

    for i in range(1, num_files + 1):
        filename = f"rst_scores_{i}.json"
        if os.path.exists(filename):
            scores_data = load_json_file(filename)
            for bug_name, confidence_value in scores_data.get("confidence", {}).items():
                confidence_sums[bug_name] += confidence_value
                confidence_counts[bug_name] += 1

    # Calculate the average confidence for each bug
    average_confidences = {bug_name: (confidence_sums[bug_name] / confidence_counts[bug_name]) 
                           for bug_name in confidence_sums}

    return average_confidences

def log_average_confidences(averages, output_filename="average_confidence_log.txt"):
    with open(output_filename, "w") as log_file:
        for bug_name, avg_confidence in sorted(averages.items(), key=lambda item: item[0]):
            log_file.write(f"{bug_name}: {avg_confidence:.4f}\n")

if __name__ == "__main__":
    final_averages = aggregate_confidence()
    log_average_confidences(final_averages)
