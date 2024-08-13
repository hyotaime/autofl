import json

def load_json_file(filename):
    with open(filename, "r") as file:
        return json.load(file)

def filter_top_methods(scores_data):
    filtered_methods = {}
    all_bug_names = set(scores_data.get("predictions", {}).keys())
    detected_bug_names = set()

    for bug_name in scores_data.get("predictions", {}):
        top_methods = {}
        bug_predictions = scores_data["predictions"].get(bug_name, {})

        for method_name, method_data in bug_predictions.items():
            rank = method_data.get("rank", 0)
            score = method_data.get("score", 0)
            if 1 <= rank <= 10 and score > 0:
                top_methods[method_name] = {
                    "autofl_rank": rank,
                    "score": score
                }

        if top_methods:
            filtered_methods[bug_name] = top_methods
            detected_bug_names.add(bug_name)

    # 파악된 버그의 개수와 파악되지 않은 버그 목록을 결과에 포함
    detected_bug_count = len(detected_bug_names)
    undetected_bug_names = list(all_bug_names - detected_bug_names)

    result = {
        "detected_bug_count": detected_bug_count,
        "undetected_bugs": undetected_bug_names,
        "filtered_methods": filtered_methods
    }

    return result

def save_filtered_methods(filtered_methods, output_filename="filtered_result.json"):
    with open(output_filename, "w") as json_file:
        json.dump(filtered_methods, json_file, indent=4)

if __name__ == "__main__":
    for i in range(1, 11):
        scores_data = load_json_file(f"rst_scores_{i}.json")
        filtered_methods = filter_top_methods(scores_data)
        save_filtered_methods(filtered_methods, f"filtered_result_{i}.json")
