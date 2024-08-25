import json


def get_answer(bug_id):
    if bug_id[0].isupper():
        bug_id = bug_id.lower().capitalize()
    with open('benchmark_line.json') as f:
        ans = json.load(f)
    return ans[bug_id]


if __name__ == '__main__':
    json_name = 'test_ten_scores'
    rst_json = {}
    matched_cnt = 0
    partially_matched_cnt = 0
    not_matched_cnt = 0
    is_matched = {}
    with open(f'linelevel/{json_name}.json', 'r') as f:
        data = json.load(f)

    for bug_id, pred_exprs in data['predictions'].items():
        pred_rst = []
        for pred_expr in pred_exprs:
            if data['predictions'][bug_id][pred_expr]['exprs'] == {}:
                continue
            file_paths = data['predictions'][bug_id][pred_expr]['exprs']
            for file_path in file_paths:
                pred_rst += data['predictions'][bug_id][pred_expr]['exprs'][file_path]
        if pred_rst:
            ans = get_answer(bug_id)
            matched, missed, wrong = 0, 0, 0
            for a in ans:
                if a in pred_rst:
                    matched += 1
                else:
                    missed += 1
            for p in pred_rst:
                if p not in ans:
                    wrong += 1

            is_matched[bug_id] = {
                'matched': matched,
                'missed': missed,
                'wrong': wrong
            }

            if matched > 0:
                if missed == 0:
                    matched_cnt += 1
                else:
                    partially_matched_cnt += 1
            else:
                not_matched_cnt += 1

    print(f'total: {len(data["predictions"])}')
    print(f'matched: {matched_cnt}')
    print(f'partially_matched: {partially_matched_cnt}')
    print(f'not_matched: {not_matched_cnt}')
    rst_json['total'] = len(data['predictions'])
    rst_json['matched'] = matched_cnt
    rst_json['partially_matched'] = partially_matched_cnt
    rst_json['not_matched'] = not_matched_cnt
    rst_json['is_matched'] = is_matched

    with open(f'linelevel/{json_name}_matched.json', 'w') as f:
        json.dump(rst_json, f, indent=4)

