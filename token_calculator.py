import json
import os

prompt_tokens, completion_tokens = 0, 0

dirs = os.listdir('linetest')
for d in dirs:
    if 'test_1' in d:
        files = os.listdir(f'linetest/{d}/gpt-4o')
        for f in files:
            with open(f'linetest/{d}/gpt-4o/{f}', 'r') as file:
                data = json.load(file)
                if 'prompt_tokens' in data and 'completion_tokens' in data:
                    prompt_tokens += data['prompt_tokens']
                    completion_tokens += data['completion_tokens']

print(f'Prompt tokens: {prompt_tokens}')
print(f'Completion tokens: {completion_tokens}')
# GPT-4o
# $0.005 per 1k prompt tokens
# $0.015 per 1k completion tokens
print(f'Total cost: ${((prompt_tokens / 1000) * 0.005) + ((completion_tokens / 1000) * 0.015)}')

# used_tokens = 0
#
# dirs = os.listdir('linetest')
# for d in dirs:
#     if 'prompt_test_2' in d:
#         files = os.listdir(f'linetest/{d}/gpt-4-turbo')
#         for f in files:
#             with open(f'linetest/{d}/gpt-4-turbo/{f}', 'r') as file:
#                 data = json.load(file)
#                 if 'used_tokens' in data:
#                     used_tokens += data['used_tokens']
#
# print(f'Used tokens: {used_tokens}')
# # $0.01 per 1k prompt tokens
# print(f'Total cost: ${((used_tokens / 1000) * 0.01)}')
