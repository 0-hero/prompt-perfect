import pandas as pd
import json
from huggingface_hub import snapshot_download

def download_dataset(repo_name, destination):
    '''
    Run git clone command with the url in the given destination
    '''
    try:
        snapshot_download(repo_id=repo_name, repo_type="dataset", local_dir=destination, local_dir_use_symlinks=False)
    except Exception as e:
        print(e)


def read_file(filepath):
    if filepath.endswith(".jsonl") or filepath.endswith(".json"):
        with open(filepath, 'r') as file:
            return [json.loads(line) for line in file]
    elif filepath.endswith(".parquet"):
        return pd.read_parquet(filepath).to_dict('records')
    else:
        raise ValueError(f"Unsupported file format: {filepath}")

def construct_prompt(row, structure):
    # Create parts based on available keys in structure
    system_part = row[structure['system']] if 'system' in structure else ""
    instruction_part = f'### Instruction\n{row[structure["instruction"]]}'
    input_part = f'{row[structure["input"]]}' if ('input' in structure and row[structure["input"]].strip() != "") else ""
    output_part = f'### Output\n{row[structure["output"]]}'

    # Construct the prompt
    prompt = f'{system_part}\n\n{instruction_part}\n\n{input_part}\n\n{output_part}'
    return prompt

class EmptyResponseError(Exception):
    pass