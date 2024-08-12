import json

benchmark_line = {}

with open("benchmark.json", "r") as f:
    benchmark_data = json.load(f)

for project, bugs in benchmark_data.items():
    if "d4j" in project:
        bug_id = project.replace("d4j_", "").capitalize()
    else:
        bug_id = project.replace("_npe", "")
    if "commonsio" in bug_id:
        bug_id = bug_id.replace("commonsio", "commons-io")
    with open(f'data/rst/{bug_id}/snippet.json', 'r') as f:
        snippet_data = json.load(f)
    rsts = []
    for bug in bugs:
        class_name = bug['class_name']
        line_num = bug['line']
        flag = bug['flag']
        for snippet in snippet_data:
            if snippet['class_name'] == class_name and int(snippet['begin_line']) < int(line_num) < int(snippet['end_line']):
                rsts.append(f"{snippet['signature']}:{line_num}")

    benchmark_line[bug_id] = rsts

    with open('benchmark_line.json', 'w') as f:
        json.dump(benchmark_line, f, indent=4)
