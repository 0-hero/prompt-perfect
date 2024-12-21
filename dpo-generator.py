from openai import OpenAI
import json
import pandas as pd
import os
from tqdm import tqdm
import time
import multiprocessing
from utils import download_dataset, read_file, construct_prompt_dpo
from prompts import generate_rejected_pair_prompt, generate_accepted_pair_prompt

# Load OpenAI API key and base URL from environment variables for better security
# TODO: The 'openai.api_base' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(base_url=os.getenv("OPENAI_API_BASE"))'
# openai.api_base = os.getenv("OPENAI_API_BASE")

# client = OpenAI(api_key="", base_url="")
client = OpenAI(api_key="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", base_url="https://api.openai.com/v1/")

def prompt(final_prompt, model):
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # seconds

    for attempt in range(MAX_RETRIES):
        try:
            chat_completion = client.chat.completions.create(model=model,
            messages=[{"role": "user", "content": final_prompt}],
            temperature=0.7,
            stream=False)

            if chat_completion.choices[0].message.content.strip() == "":
                raise ValueError("Empty or whitespace-only response from the API")

            return chat_completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error: {e}")
            if attempt < MAX_RETRIES - 1:
                print(f"Retrying... ({attempt + 1}/{MAX_RETRIES})")
                time.sleep(RETRY_DELAY)
            else:
                print("Max retries reached. Exiting...")
                break
    return None  # Return None if all retries fail

def process_row(row, dataset_details):
    try:
        dataset_prompt, output = construct_prompt_dpo(row, dataset_details)
        if row['extracted_score'] in [1, 2, 3]:
            # print("Generated accepted pair")
            final_prompt = generate_accepted_pair_prompt.format(instruction=dataset_prompt)
            # print(final_prompt)
            response = prompt(final_prompt, "gpt-4-0125-preview")
            # print(response)
            row["accepted_pair"] = response
            row["rejected_pair"] = output
            row["generated"] = "accepted_pair"
            row["generator_model"] = "gpt-4-0125-preview"
        elif row['extracted_score'] in [4, 5]:
            # print("Generated Rejected pair")
            final_prompt = generate_rejected_pair_prompt.format(instruction=dataset_prompt)
            # print(final_prompt)
            response = prompt(final_prompt, "gpt-3.5-turbo-0125")
            # print(response)
            row["accepted_pair"] = output
            row["rejected_pair"] = response
            row["generated"] = "rejected_pair"
            row["generator_model"] = "gpt-3.5-turbo-0125"
    except Exception as e:
        print("Error processing row:", e)
    return row

def worker_batch(batch_data):
    batch, dataset_details = batch_data
    return [process_row(row, dataset_details) for row in batch]

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def main():
    batch_size = 100
    with open('datasets.json', 'r') as file:
        data = json.load(file)

    for dataset_name, dataset_details in data.items():
        if not dataset_details.get("skip", False):
            destination = os.path.join("datasets", dataset_name)
            for location in dataset_details.get("locations", []):
                file_path = os.path.join(destination, location)
                print(f"Processing file: {file_path}")
                rows = read_file(file_path)
                # rows = pd.DataFrame(rows)
                
                # Remove rows with 'extracted_score' of 3
                # rows = rows[rows['extracted_score'] != 3]

                # Convert DataFrame back to a list of dictionaries
                # rows = rows.to_dict('records')
                
                batched_data = [(batch, dataset_details) for batch in chunks(rows, batch_size)]
                total_batches = len(batched_data)
                all_processed_rows = []

                with tqdm(total=total_batches) as pbar:
                    with multiprocessing.Pool() as pool:  # Let Pool decide the number of processes
                        results = []

                        def update(result):
                            all_processed_rows.extend(result)
                            pbar.update()

                        for bd in batched_data:
                            result = pool.apply_async(worker_batch, args=(bd,), callback=update)
                            results.append(result)

                        for result in results:
                            result.wait()

                # File writing logic based on file extension
                if file_path.endswith(".jsonl") or file_path.endswith(".json"):
                    new_file_path = file_path.rsplit('.', 1)[0] + "_dpo." + file_path.rsplit('.', 1)[1]
                    with open(new_file_path, 'w') as file:
                        for row in all_processed_rows:
                            file.write(json.dumps(row) + "\n")
                elif file_path.endswith(".parquet"):
                    df = pd.DataFrame(all_processed_rows)
                    new_file_path = file_path.replace(".parquet", "_dpo.parquet")
                    df.to_parquet(new_file_path)

                with open('done.txt', 'a') as f:  # Use 'a' to append to the file
                    f.write(dataset_name + " " + location + "\n")

if __name__ == "__main__":
    main()
