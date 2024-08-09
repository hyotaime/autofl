import os
import json
import paramiko

def load_server_info(filename="server_info.txt"):
    with open(filename, "r") as f:
        lines = f.readlines()
    server_info = {}
    for line in lines:
        key, value = line.strip().split('=')
        server_info[key.strip()] = value.strip()
    return server_info

def fetch_diff_files_from_server(server_info, bug_dict):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        server_info['host'], 
        username=server_info['username'], 
        password=server_info['password'], 
        port=int(server_info['port'])
    )

    sftp = ssh.open_sftp()
    base_dir = "/data/bug_db/subjects"
    diff_data = {}

    for project, bugs in bug_dict.items():
        for bug in bugs:
            diff_file_path = f"{base_dir}/{project.lower()}/{bug}/diff_{bug}.txt"
            print(f"Searching for file: {diff_file_path}")  # 탐색하는 경로 출력

            try:
                with sftp.file(diff_file_path, "r") as diff_file:
                    diff_content = diff_file.read().decode('utf-8')  # 바이트 데이터를 문자열로 변환
                    diff_data[f"{project}/{bug}"] = diff_content
            except FileNotFoundError:
                print(f"File not found: {diff_file_path}")

    sftp.close()
    ssh.close()
    
    return diff_data

def save_to_json(diff_data, output_filename="diff_data.json"):
    with open(output_filename, "w") as json_file:
        json.dump(diff_data, json_file, indent=4)

if __name__ == "__main__":
    bug_dict = {
    "lang": [
        "lang_npe_1", "lang_npe_2", "lang_npe_3", "lang_npe_4", "lang_npe_5", 
        "lang_npe_6", "lang_npe_7", "lang_npe_8", "lang_npe_9", "lang_npe_10", 
        "lang_npe_11", "lang_npe_12", "lang_npe_13"
    ],
    "math": [
        "math_npe_1", "math_npe_2", "math_npe_3"
    ],
    "collections": [
        "collections_npe_1", "collections_npe_2", "collections_npe_3"
    ],
    "commons-io": [
        "commons-io_npe_1", "commons-io_npe_2", "commons-io_npe_3", "commons-io_npe_4", "commons-io_npe_5",
        "commons-io_npe_6", "commons-io_npe_7", "commons-io_npe_8", "commons-io_npe_9", "commons-io_npe_10",
        "commons-io_npe_11", "commons-io_npe_12", "commons-io_npe_13", "commons-io_npe_14", "commons-io_npe_15",
        "commons-io_npe_16", "commons-io_npe_17", "commons-io_npe_18", "commons-io_npe_19"
    ],
    "defects4j": [
        "Chart-2", "Chart-4", "Chart-14", "Chart-16", "Cli-5", 
        "Cli-30", "Closure-2", "Closure-171", "Codec-5", "Codec-13", 
        "Codec-17", "Csv-4", "Csv-9", "Csv-11", "Gson-6", 
        "Gson-9", "JacksonCore-8", "JacksonDatabind-3", "JacksonDatabind-13", 
        "JacksonDatabind-36", "JacksonDatabind-80", "JacksonDatabind-93", 
        "JacksonDatabind-95", "JacksonDatabind-107", "Jsoup-8", "Jsoup-22", 
        "Jsoup-26", "Jsoup-66", "Jsoup-89", "Lang-20", "Lang-33", 
        "Lang-39", "Lang-47", "Lang-57", "Math-4", "Math-70", 
        "Math-79", "Mockito-18", "Mockito-38"
    ]

    }

    server_info = load_server_info()
    diff_data = fetch_diff_files_from_server(server_info, bug_dict)
    save_to_json(diff_data)
