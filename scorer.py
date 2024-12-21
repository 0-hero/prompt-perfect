import openai
from openai import OpenAI
import json
from utils import download_dataset, read_file, construct_prompt
from prompts import score_prompt_original, score_prompt_conversation, score_prompt_coding, score_prompt_math, score_prompt_function_calling, score_prompt_science, score_prompt_agents, score_prompt_sql
import pandas as pd
import os
from tqdm import tqdm
import time
import ast
import multiprocessing

# client = OpenAI(
#     api_key="SampleKey",
#     base_url="https://api.deepinfra.com/v1/openai"
# )

client = OpenAI(
    api_key="NA",
)

# def prompt(final_prompt, model="cognitivecomputations/dolphin-2.6-mixtral-8x7b"):
def prompt(final_prompt, model="gpt-3.5-turbo-0125"):
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # seconds

    for attempt in range(MAX_RETRIES):
        try:
            chat_completion = client.chat.completions.create(model=model,
            messages=[{"role": "user", "content": final_prompt}],
            temperature=0.7,
            stream=False)

            # print(chat_completion.choices[0].message.content)

            # Check if the response is empty or just whitespace
            if (chat_completion.choices[0].message.content.strip()=="" or chat_completion.choices[0].message.content.strip()=="\n"):
                raise ValueError("Empty or whitespace-only response from the API")

            # if isinstance(chat_completion, dict):
            #     print(True)
            #     # not stream
            #     return chat_completion.choices[0].message.content.strip()
            return chat_completion.choices[0].message.content.strip()
            # else:
            #     # stream
            #     content_list = []
            #     for token in chat_completion:
            #         content = token.choices[0].delta.content
            #         if content and content.strip():
            #             content_list.append(content.strip())
            #     return ''.join(content_list)

        except Exception as e:
            print(f"Error: {e}")
            if attempt < MAX_RETRIES - 1:
                print(f"Retrying... ({attempt + 1}/{MAX_RETRIES})")
                time.sleep(RETRY_DELAY)
            else:
                print("Max retries reached. Exiting...")
                break
    return None  # Return None if all retries fail

def process_score(response):
    extract_score_prompt = '''Extract only the score from the given context as an integer. If the text mentions anything related to 'rate limit', if the context is empty, if no score is mentioned in context respond with a score of 0. Score must be either 0,1,2,3,4,5.

--- Context Start ---
{context}
--- Context End ---

Extracted Score as Integer:'''
    final_prompt = extract_score_prompt.format(context=response)
    # print(final_prompt)
    response = None
    retries = 5
    while retries > 0:
        response = prompt(final_prompt)
        # print(response)
        try:
            score = int(response.strip())
            return score
        except ValueError:
            retries -= 1
            if retries == 0:
                print("Failed to extract score from prompt. Setting score to 0.")
                return 0
            else:
                print("Invalid response from prompt. Retrying...")
        except:
            retries -= 1
            if retries == 0:
                print("Failed to extract score from prompt. Setting score to 0.")
                return 0
            else:
                print("Invalid response from prompt. Retrying...")
            
    return 0

# Code to re-run failed rows
# def process_row(row, dataset_details, score_prompt):
#     if row['extracted_score'] not in [1,2,3,4,5]:
#         none_counter = 0
#         dataset_prompt = construct_prompt(row, dataset_details) 
#         final_prompt = score_prompt.format(instruction=dataset_prompt)
#         response = prompt(final_prompt)
#         # print(response)
#         if response is None:
#             none_counter += 1
#         row["score"] = response
#         row["extracted_score"] = process_score(response)
#         # print(row)
#         return row
#     return row

# Code to for openhermes filtering
# def process_row(row, dataset_details, score_prompt):
#     try:
#         # print(row['source'])
#         if ('source' not in row) or (row['source'] in ['caseus_custom', 'nan', None, 'Econ_domain_expert', 'GPT-4 Comparison Data', 'LMSys Chatbot Arena', 'CogStackMed', 'UnnaturalInstructions', 'cot_alpaca_gpt4']):
#             none_counter = 0
#             dataset_prompt = construct_prompt(row, dataset_details) 
#             final_prompt = score_prompt.format(instruction=dataset_prompt)
#             response = prompt(final_prompt)
#             # print(response)
#             if response is None:
#                 none_counter += 1
#             row["score"] = response
#             time.sleep(1)
#             # row["extracted_score"] = process_score(response)
#             # print(row)
#             return row
#         return None
#     except Exception as e:
#         print(row)
#         print("Error processing row:", e)
# 
#         return None

# Scoring agents
# def process_row(row, dataset_details, score_prompt):
#     try:
#         # txts = row['chat'].split("<|endoftext|>")
#         # print(str(row['system']) + "\n" + str("\n".join(txts)))
#         # print(row['text'])
#         # print("---------------")
#         none_counter = 0
#         # print(ast.literal_eval(row['text'])['instruction'])
#         # dataset_prompt = construct_prompt(row['text'], dataset_details)
#         # print(dataset_prompt)
#         dataset_prompt = construct_prompt(ast.literal_eval(row['text']), dataset_details) 
#         # dataset_prompt = str(row['sample'])
#         # dataset_prompt = str(row['system']) + "\n" + str("\n".join(txts))
#         # dataset_prompt = ast.literal_eval(row['text'])
#         final_prompt = score_prompt.format(instruction=dataset_prompt)
#         response = prompt(final_prompt)
#         # print(response)
#         if response is None:
#             none_counter += 1
#         row["score"] = response
#         time.sleep(1)
#         # row["extracted_score"] = process_score(response)
#         # print(row)
#         return row
#     except Exception as e:
#         print("Error processing row:", e)
#         return row

def process_row(row, dataset_details, score_prompt):
    try:
        none_counter = 0
        dataset_prompt = construct_prompt(row, dataset_details) 
        final_prompt = score_prompt.format(instruction=dataset_prompt)
        # print(final_prompt)
        # print("-----------------")
        response = prompt(final_prompt)
        # print(response)
        if response is None:
            none_counter += 1
        row["score"] = response
        time.sleep(1)
        # row["extracted_score"] = process_score(response)
        # print(row)
        return row
    except Exception as e:
        print("Error processing row:", e)
        return row

def worker_batch(batch_data):
    batch, dataset_details, score_prompt = batch_data
    return [process_row(row, dataset_details, score_prompt) for row in batch]

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def main():
    batch_size = 100
    with open('datasets.json', 'r') as file:
        data = json.load(file)

    for dataset_name, dataset_details in data.items():
        if not dataset_details["skip"]:
            hf_hub = dataset_details["hf_hub"]
            destination = os.path.join("datasets", dataset_name)
            if "prompt_type" in dataset_details:
                if dataset_details["prompt_type"] == "conversation":
                    score_prompt = score_prompt_conversation
                elif dataset_details["prompt_type"] == "coding":
                    score_prompt = score_prompt_coding
                elif dataset_details["prompt_type"] == "math":
                    score_prompt = score_prompt_math
                elif dataset_details["prompt_type"] == "function_calling":
                    score_prompt = score_prompt_function_calling
                elif dataset_details["prompt_type"] == "science":
                    score_prompt = score_prompt_science
                elif dataset_details["prompt_type"] == "agents":
                    score_prompt = score_prompt_agents
                elif dataset_details["prompt_type"] == "sql":
                    score_prompt = score_prompt_sql
            else:
                score_prompt = score_prompt_original
            # download_dataset(hf_hub, destination)
            for location in dataset_details["locations"]:
                file_path = os.path.join(destination, location)
                print(file_path)
                rows = read_file(file_path)
                # Store results of all batches temporarily
                batched_data = [(batch, dataset_details, score_prompt) for batch in chunks(rows, batch_size)]
                total_batches = len(batched_data)
                all_processed_rows = []
                new_file_path = None
                with tqdm(total=total_batches) as pbar:
                    with multiprocessing.Pool(processes=30) as pool:
                        results = []

                        def update(result):
                            all_processed_rows.extend(result)
                            pbar.update()

                        for bd in batched_data:
                            result = pool.apply_async(worker_batch, args=(bd,), callback=update)
                            results.append(result)

                        # Wait for all tasks to complete
                        for result in results:
                            result.wait()
                # Revised file writing logic
                if file_path.endswith(".jsonl") or file_path.endswith(".json"):
                    new_file_path = file_path.replace(".jsonl", "_processed.jsonl") if file_path.endswith(".jsonl") else file_path.replace(".json", "_processed.json")
                    with open(new_file_path, 'w') as file:
                        for row in all_processed_rows:
                            file.write(json.dumps(row) + "\n")

                elif file_path.endswith(".parquet"):
                    df = pd.DataFrame(all_processed_rows)
                    new_file_path = file_path.replace(".parquet", "_processed.parquet")
                    df.to_parquet(new_file_path)
                with open('done.txt', 'w') as f:
                    f.write(dataset_name + " " + location)

if __name__ == "__main__":
    main()