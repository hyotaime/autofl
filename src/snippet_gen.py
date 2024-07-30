import os
import json
import re
from server import Server
import bug_list
from collections import deque

# 주석 추출 함수
def extract_comments(lines, m_line_idx):
    comments = deque()
    inside_comment = False
    for i in range(m_line_idx - 1, -1, -1):
        line = lines[i]
        if line.strip().endswith("*/") or line.strip().startswith("//"):
            inside_comment = True
        if inside_comment:
            comments.appendleft(line.replace("/**", "").replace("*/", "").replace("//", ""))
        if line.strip().startswith("/*") or line.strip().startswith("//"):
            break
    return "\n".join(comments)


# 필드 정보 추출 함수
def extract_field_info(file_lines, class_name, src_path):
    fields = []
    method_pattern = re.compile(
        r'^\s*(public|protected|private)?\s*(static)?\s*[\w\<\>\[\]]+\s+(\w+)\s*\(([^)]*)\)\s*\{')

    for i, line in enumerate(file_lines):
        match = method_pattern.match(line)
        if match:
            method_name = f"{match.group(3)}({match.group(4).strip()})"
            snippet = line.strip()
            j = i + 1
            child_range = []
            while file_lines[j].strip().endswith(";") or not file_lines[j].strip():
                snippet += "\n" + file_lines[j].strip()
                start_col = 0
                for k in range(len(file_lines[j])):
                    if file_lines[j][k] != ' ':
                        start_col = k + 1
                        break
                child_range.append(f'(line {j + 1},col {start_col})-(line {j + 1},col {len(file_lines[j])})')
                j += 1
            snippet += "\n" + file_lines[j].strip()
            fields.append({
                "class_name": class_name,
                "child_classes": [],
                "src_path": src_path,
                "signature": f'{class_name}.{method_name}',
                "snippet": snippet,
                "begin_line": i + 1,
                "end_line": j + 1,
                "comment": extract_comments(file_lines, i),
                "child_ranges": child_range
            })
    return fields


def select_src_path(bug_id, class_name):
    paths = [
        "source",
        "fixed/src/test/java",
        "buggy/src/test",
        "fixed/src/main/java",
        "fixed/src/test",
        "buggy/mockmaker/bytebuddy/main/java" if bug_id == "Mockito-18" else None,
        "buggy/cglib-and-asm/src" if bug_id == "Mockito-38" else None
    ]
    for path in paths:
        if path:
            src_path = f"{remote_dir}/{path}/{class_name.replace('.', '/')}.java"
            try:
                server.read_remote_file(src_path)
                return src_path
            except FileNotFoundError:
                continue
    raise FileNotFoundError(f"Source file for {class_name} in bug {bug_id} not found in any of the paths.")


if __name__ == '__main__':
    specific_bugs = ["Mockito-18", "Mockito-38"]
    bug_id_list = bug_list.get_d4j_bug_list()

    for bug_id in specific_bugs:
        if bug_id in bug_id_list:
            print(f"Generating snippet for {bug_id}...", end='')

            # 서버 접속 정보 설정
            remote_dir = f'/data/bug_db/subjects/defects4j/{bug_id}'

            server = Server()

            try:
                npe_traces_content = json.loads(server.read_remote_file(f'{remote_dir}/npe.traces.json'))
                coverage_content = json.loads(server.read_remote_file(f'{remote_dir}/coverage.json'))
                tests_content = json.loads(server.read_remote_file(f'{remote_dir}/tests.json'))

                failed_tests = {test['name']: test for test in tests_content['failed.tests']}
                coverage_lines = {item['className']: item['covered'] for item in coverage_content['coverage']}

                snippets = []

                for trace in npe_traces_content['npe.traces']:
                    test_method = trace['test.method']
                    is_bug = test_method in failed_tests

                    for t in trace['traces']:
                        if t['is_target'] and t['line'] in coverage_lines.get(t['class'], []):
                            src_path = select_src_path(bug_id, t['class'])
                            class_file_content = server.read_remote_file(src_path)
                            class_file_lines = class_file_content.splitlines()
                            snippet = {
                                'name': f'{t["class"]}.join#{t["line"]}',
                                'is_bug': is_bug,
                                'src_path': src_path,
                                'class_name': t['class'],
                                'signature': f'{t["class"]}.join(...)',
                                'snippet': '',
                                'begin_line': t['line'],
                                'end_line': t['line'] + 1,
                                'comment': '',
                                'resolved_comments': {},
                                'susp': {'ochiai_susp': 0.5},
                                'num_failing_tests': 0 if is_bug else 1
                            }
                            snippets.append(snippet)

                with open(f'snippet_{bug_id}.json', 'w') as f:
                    json.dump(snippets, f, indent=4)

                print(f"Snippet for {bug_id} generated.")

            except FileNotFoundError as e:
                print(f"Error loading files for {bug_id}: {e}")
            except Exception as e:
                print(f"An error occurred for {bug_id}: {e}")
