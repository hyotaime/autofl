import json

def load_json_file(filename):
    with open(filename, "r") as file:
        return json.load(file)

def map_bug_name(bug_name):
    # 버그 이름 맵핑 로직
    if bug_name.startswith("lang_npe_"):
        return bug_name.replace("lang_npe_", "lang_")
    if bug_name.startswith("math_npe_"):
        return bug_name.replace("math_npe_", "math_")
    return bug_name

def compare_methods(filtered_methods, diff_data):
    comparison_result = {}

    for bug_name, methods in filtered_methods.items():
        mapped_bug_name = map_bug_name(bug_name)
        diff_methods = diff_data.get(mapped_bug_name, [])

        matched_methods = []
        partially_matched_methods = []
        not_matched_methods = []

        for method_name in methods.keys():
            method_base = method_name.split('(')[0]  # 메소드 시그니처에서 메소드 이름만 추출
            if any(diff_method.startswith(method_base) for diff_method in diff_methods):
                if any(diff_method == method_name for diff_method in diff_methods):
                    matched_methods.append(method_name)
                else:
                    partially_matched_methods.append(method_name)
            else:
                not_matched_methods.append(method_name)

        if matched_methods:
            comparison_result[bug_name] = {
                "Matched": matched_methods
            }
        if partially_matched_methods:
            comparison_result.setdefault(bug_name, {}).update({
                "Partially Matched": partially_matched_methods
            })
        if not_matched_methods:
            comparison_result.setdefault(bug_name, {}).update({
                "Not Matched": not_matched_methods
            })

    return comparison_result

def save_comparison_result(comparison_result, output_filename="comparison_result.json"):
    with open(output_filename, "w") as json_file:
        json.dump(comparison_result, json_file, indent=4)

if __name__ == "__main__":
    filtered_methods = load_json_file("filtered_result_7.json")
    diff_data = load_json_file("diff_data.json")

    comparison_result = compare_methods(filtered_methods["filtered_methods"], diff_data)
    save_comparison_result(comparison_result, "comparison_result_7.json")
