import openai
import json
from utils import download_dataset, read_file, construct_prompt
from prompts import score_prompt
import pandas as pd
import os
from tqdm import tqdm
import time
import fastparquet

openai.api_key = ""
openai.api_base = "http://localhost:1337"

def prompt(final_prompt, model="gpt-3.5-turbo-16k"):
    MAX_RETRIES = 10
    RETRY_DELAY = 0.5  # seconds

    for attempt in range(MAX_RETRIES):
        try:
            chat_completion = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": final_prompt}],
                stream=False,
            )

            # Check if the response is empty or just whitespace
            if (not chat_completion 
                or 'choices' not in chat_completion 
                or not chat_completion['choices'] 
                or not chat_completion['choices'][0]['message']['content'].strip()):
                raise ValueError("Empty or whitespace-only response from the API")

            if isinstance(chat_completion, dict):
                # not stream
                return chat_completion['choices'][0]['message']['content'].strip()
            else:
                # stream
                content_list = []
                for token in chat_completion:
                    content = token["choices"][0]["delta"].get("content")
                    if content and content.strip():
                        content_list.append(content.strip())
                return ''.join(content_list)

        except Exception as e:
            print(f"Error: {e}")
            if attempt < MAX_RETRIES - 1:
                print(f"Retrying... ({attempt + 1}/{MAX_RETRIES})")
                time.sleep(RETRY_DELAY)
            else:
                print("Max retries reached. Exiting...")
                break
    return None  # Return None if all retries fail


def main():
    n=10
    with open('dataset_formats.json', 'r') as file:
        data = json.load(file)
    
    for dataset_name, dataset_details in data.items():
        if not dataset_details["skip"]:
            # Step 1: Download the dataset
            hf_hub = dataset_details["hf_hub"]
            destination = os.path.join("datasets", dataset_name)

            # download_dataset(f"https://huggingface.co/datasets/{hf_hub}", destination)
            download_dataset(hf_hub,destination)
            for location in dataset_details["locations"]:
                # Step 2: Read the file
                file_path = os.path.join(destination, location)
                print(file_path)
                rows = read_file(file_path)
                
                # Step 3 and 4: Construct prompt and get response
                counter = 0
                new_file_path = None
                new_rows = []
                none_counter = 0
                for row in tqdm(rows):
                    if none_counter>10:
                        break
                    dataset_prompt = construct_prompt(row, dataset_details["structure"])
                    final_prompt = score_prompt + dataset_prompt
                    # print(final_prompt)
                    response = prompt(final_prompt)
                    if response is None:
                        none_counter += 1
                    print(response)
                    # Append the response to the row (modify based on your requirements)
                    row["score"] = response
                    
                    # Step 5: Write the new dataset after every n rows
                    counter += 1
                    new_rows.append(row)
                    if counter == n:
                        if file_path.endswith(".jsonl"):
                            if new_file_path is None:
                                new_file_path = file_path.replace(".jsonl", f"_temp.jsonl")
                                with open(new_file_path, 'w') as file:
                                    for r in new_rows:
                                        file.write(json.dumps(r) + "\n")
                            else:
                                with open(new_file_path, 'a') as file:
                                    for r in new_rows:
                                        file.write(json.dumps(r) + "\n")
                            new_rows = []
                            counter = 0
                        elif file_path.endswith(".parquet"):
                            df = pd.DataFrame(new_rows)
                            if new_file_path is None:
                                new_file_path = file_path.replace(".parquet", f"_temp.parquet")
                                df.to_parquet(new_file_path)
                            else:
                                if file_path.endswith(".parquet"):
                                    if new_file_path is None:
                                        df = pd.DataFrame(rows)
                                        df.to_parquet(file_path)
                                    else:
                                        # Append to existing file if it exists
                                        if os.path.exists(file_path):
                                            existing_df = fastparquet.ParquetFile(file_path).to_pandas()
                                            df = pd.concat([existing_df, pd.DataFrame(new_rows)])
                                        else:
                                            df = pd.DataFrame(new_rows)
                                        df.to_parquet(new_file_path)
                            new_rows = []
                            counter = 0

                        # Step 5: Write the new dataset
                        if file_path.endswith(".jsonl"):
                            if new_file_path is None:
                                with open(file_path, 'w') as file:
                                    for row in rows:
                                        file.write(json.dumps(row) + "\n")
                            else:
                                os.remove(file_path)
                                os.rename(new_file_path, file_path)
                        elif file_path.endswith(".parquet"):
                            if new_file_path is None:
                                df = pd.DataFrame(rows)
                                df.to_parquet(file_path)
                            else:
                                os.remove(file_path)
                                os.rename(new_file_path, file_path)

if __name__ == "__main__":
    main()
    # print(prompt("Hi there! How are you?"))