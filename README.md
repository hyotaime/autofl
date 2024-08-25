# AutoFL in Line Level

> This repository contains modifications to the original AutoFL to line level.

The original AutoFL implementation can be found at [coinse/autofl](https://github.com/coinse/autofl).

# Environmental Setup
## Python Dependencies
- Compatible with Python >= 3.10
- Compatible with `openai>=0.27.8,<=0.28.1` (not compatible with `openai>=1.0.0`)

Install the required dependencies using the following command:

```shell
python -m pip install pandas python-dotenv tqdm markdown2 tiktoken "openai>=0.27.8,<=0.28.1" javalang-ext scipy numpy matplotlib jupyter seaborn nbformat
```

## OpenAI API Setup
Before using AutoFL, set up your OpenAI API credentials by creating a `.env` file with the following content:

```shell
OPENAI_API_KEY={YOUR_API_KEY}
OPENAI_ORG_KEY={YOUR_ORG_KEY} # Optional
```
Replace `{YOUR_API_KEY}` with your OpenAI API key and `{YOUR_ORG_KEY}` with your organization's API key.

# General Usage

## Run AutoFL

To run AutoFL, use the following command:
```shell
sh line_runner.sh {expr_label} {num_repetitions} {dataset}
```

Replace `{expr_label}` with a label for your experiment, `{num_repetitions}` with the number of repetitions, and `{dataset}` with the dataset you want to use (e.g. `rst`).

## Compute Scores
```shell
python compute_score.py {result_directories} -l java -a -v -o {json_output_file}
```

`{result_directories}` should be the directories containing your AutoFL result files.
- `-l` specifies the language (`java`).
- `-a` enables the use of auxiliary scores to break ties.
- `-v` enables verbose mode.
- `-o` specifies the path to the JSON output file.

## Examples

- Defects4J and Apache dataset:
    ```shell
    sh line_runner.sh my_d4j_autofl_ 5 rst
    python compute_score.py linelevel/my_d4j_autofl_*/gpt-4o -l java -a -v -o scores.json
    ```
