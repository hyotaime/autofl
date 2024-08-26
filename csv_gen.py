import pandas as pd
import json

file_name = "test_ten_scores_matched"
with open(f'linelevel/{file_name}.json', 'r') as f:
    data = json.load(f)

data = data['is_matched']
df = pd.DataFrame(columns=['bug_name', 'is_matched', 'matched', 'missed', 'wrong'])

for i, bug in enumerate(data):
    if data[bug]['matched'] > 0 and data[bug]['missed'] == 0:
        is_matched = 'matched'
    elif data[bug]['matched'] > 0 and data[bug]['missed'] > 0:
        is_matched = 'partially matched'
    else:
        is_matched = 'not matched'
    df.loc[i] = [bug, is_matched, data[bug]['matched'], data[bug]['missed'], data[bug]['wrong']]

df.to_csv(f'linelevel/{file_name}.csv', index=False)
