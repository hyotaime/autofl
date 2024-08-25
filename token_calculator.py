import json
import os

prompt_tokens, completion_tokens = 0, 0

dirs = os.listdir('linelevel')
for d in dirs:
    if os.path.isdir(f'linelevel/{d}/gpt-4o'):
        files = os.listdir(f'linelevel/{d}/gpt-4o')
        for f in files:
            with open(f'linelevel/{d}/gpt-4o/{f}', 'r') as file:
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
