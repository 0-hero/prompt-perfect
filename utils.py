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
    if filepath.endswith(".jsonl"):
        with open(filepath, 'r') as file:
            return [json.loads(line) for line in file]
    elif filepath.endswith(".json"):
        with open(filepath, 'r') as file:
            return json.load(file)  # Note the change here from json.loads to json.load
    elif filepath.endswith(".parquet"):
        return pd.read_parquet(filepath, engine='pyarrow').to_dict('records')
    else:
        raise ValueError(f"Unsupported file format: {filepath}")

def construct_prompt(row, dataset_details):
    # Create parts based on available keys in structure
    if "structure_type" in dataset_details:
        if dataset_details["structure_type"] == "multiturn-conversation":
            # system_part = None
            # instruction_part = None
            # output_part = None 
            out_message = ""
            for message in row["conversations"]:
                if message['from'] == 'system':
                    # system_part = message['value']
                    out_message += f"System : {message['value']}\n"
                elif message['from'] == 'human':
                    # instruction_part = f"### Instruction\n {message['value']}"
                    out_message += f"Human : {message['value']}\n"
                elif message['from'] == 'function-call':
                    out_message += f"Function : {message['value']}\n"
                elif message['from'] == 'function-response':
                    out_message += f"Function Response : {message['value']}\n"
                elif message['from'] == 'gpt':
                    # output_part = f"### Output\n {message['value']}"
                    out_message += f"AI Bot : {message['value']}\n"
            # Construct the prompt
            # prompt = f'{system_part}\n\n{instruction_part}\n\n{output_part}'
            prompt = out_message
            return prompt
        
        elif dataset_details["structure_type"] == "multiturn-capybara":
            prompt = ""
            for message in row["conversation"]:
                prompt += f"Human : {message['input']}\nAI Bot : {message['output']}\n"
            return prompt
        elif dataset_details["structure_type"] == "multiturn-ultrachat":
            prompt = ""
            for message in row["messages"]:
                if message['role'] == 'user':
                    prompt += f"Human : {message['content']}\n" 
                elif message['role'] == 'assistant':
                    prompt += f"AI Bot : {message['content']}\n"
            return prompt
        elif dataset_details["structure_type"] == "multiturn-lmsys":
            prompt = ""
            for message in row["conversation"]:
                if message['role'] == 'user':
                    prompt += f"Human : {message['content']}\n" 
                elif message['role'] == 'assistant':
                    prompt += f"AI Bot : {message['content']}\n"
            return prompt
        elif dataset_details["structure_type"] == "multiturn-programming":
            prompt = ""
            for message in row["conversations"]:
                if message['from'] == 'human':
                    prompt += f"Human : {message['text']}\n" 
                elif message['from'] == 'assistant':
                    prompt += f"AI Bot : {message['text']}\n"
            return prompt

    # print(row)
    # print("--------")
    structure = dataset_details["structure"]
    system_part = row[structure['system']] if 'system' in structure else ""
    instruction_part = f'### Instruction\n{row[structure["instruction"]]}'
    input_part = f'{row[structure["input"]].strip()}' if ('input' in structure and row[structure["input"]] is not None and row[structure["input"]].strip() != "") else ""
    output_part = f'### Output\n{row[structure["output"]]}' if 'output' in structure else ""

    # Construct the prompt
    prompt = f'{system_part}\n\n{instruction_part}\n\n{input_part}\n\n{output_part}'
    return prompt

def construct_prompt_dpo(row, dataset_details):
    # Create parts based on available keys in structure
    if "structure_type" not in dataset_details:
        structure = dataset_details["structure"]
        system_part = f'### System\n{row[structure["system"]]}' if 'system' in structure else ""
        instruction_part = f'### Instruction\n{row[structure["instruction"]]}'
        input_part = f'{row[structure["input"]].strip()}' if ('input' in structure and row[structure["input"]] is not None and row[structure["input"]].strip() != "") else ""
        output_part = f'### Output\n'

        # Construct the prompt
        prompt = f'{system_part}\n\n{instruction_part}\n\n{input_part}\n\n{output_part}'
        return prompt, row[structure["output"]]

class EmptyResponseError(Exception):
    pass