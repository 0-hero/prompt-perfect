import openai
import json
from utils import download_dataset, read_file, construct_prompt
from prompts import score_prompt
import pandas as pd
import os
from tqdm import tqdm
import time
from concurrent.futures import ThreadPoolExecutor
import fastparquet

openai.api_key = ""
openai.api_base = "http://localhost:1337"

os.environ["TRANSFORMERS_CACHE"] = "/mnt/volume_sfo3_01"

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

def process_row(row, dataset_details, score_prompt):
    none_counter = 0
    dataset_prompt = construct_prompt(row, dataset_details["structure"])
    final_prompt = score_prompt + dataset_prompt
    response = prompt(final_prompt)
    # print(response)
    if response is None:
        none_counter += 1
    row["score"] = response
    # print(row)
    return row

def worker_batch(batch_data):
    batch, dataset_details, score_prompt = batch_data
    return [process_row(row, dataset_details, score_prompt) for row in batch]

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def main():
    batch_size = 10
    with open('dataset_formats.json', 'r') as file:
        data = json.load(file)

    for dataset_name, dataset_details in data.items():
        if not dataset_details["skip"]:
            hf_hub = dataset_details["hf_hub"]
            destination = os.path.join("datasets", dataset_name)
            download_dataset(hf_hub, destination)
            for location in dataset_details["locations"]:
                file_path = os.path.join(destination, location)
                print(file_path)
                rows = read_file(file_path)
                
                # Store results of all batches temporarily
                all_processed_rows = []
                new_file_path = None
                # Chunk rows into batches of 8
                for batch in tqdm(chunks(rows, batch_size), total=len(rows)//batch_size + (len(rows)%batch_size > 0)):
                    # Process batches in parallel
                    with ThreadPoolExecutor() as executor:
                        batch_results = executor.map(worker_batch, [(batch, dataset_details, score_prompt)])
                        for processed_batch in batch_results:
                            # print(processed_batch)
                            if file_path.endswith(".jsonl"):
                                if new_file_path is None:
                                    new_file_path = file_path.replace(".jsonl", f"_temp.jsonl")
                                    with open(new_file_path, 'w') as file:
                                        for r in processed_batch:
                                            file.write(json.dumps(r) + "\n")
                                else:
                                    with open(new_file_path, 'a') as file:
                                        for r in processed_batch:
                                            file.write(json.dumps(r) + "\n")
                            
                            elif file_path.endswith(".json"):
                                if new_file_path is None:
                                    new_file_path = file_path.replace(".json", f"_temp.json")
                                    with open(new_file_path, 'w') as file:
                                        for r in processed_batch:
                                            file.write(json.dumps(r) + "\n")
                                else:
                                    with open(new_file_path, 'a') as file:
                                        for r in processed_batch:
                                            file.write(json.dumps(r) + "\n")

                            elif file_path.endswith(".parquet"):
                                df = pd.DataFrame(processed_batch)
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
                                                df = pd.concat([existing_df, pd.DataFrame(processed_batch)])
                                            else:
                                                df = pd.DataFrame(processed_batch)
                                            df.to_parquet(new_file_path)

                            all_processed_rows.extend(processed_batch)

                # Handle writing logic based on file type
                if file_path.endswith(".jsonl") or file_path.endswith(".json"):
                    with open(file_path, 'w') as file:
                        for row in all_processed_rows:
                            file.write(json.dumps(row) + "\n")
                elif file_path.endswith(".parquet"):
                    df = pd.DataFrame(all_processed_rows)
                    df.to_parquet(file_path)

if __name__ == "__main__":
    main()