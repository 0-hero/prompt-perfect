# Scoring popular datasets with ["Self-Alignment with Instruction Backtranslation"](https://arxiv.org/abs/2308.06259) prompt

### 35 datasets scored (>6B tokens)
Scored Dataset on [HuggingFace](https://huggingface.co/datasets/0-hero/prompt-perfect)
## Scoring Models used
- gpt-3.5-turbo-16k
- gpt-3.5-turbo-1106
- gpt-3.5-turbo-0125

## All datasets have 2 additional columns
- score - Response from the model including CoT (if provided)
- extracted_score - Extracted score from the score column as int
## Datasets Scored by Prompt (Needs to be updated)
#### Original Score Prompt from paper
- [airoboros-2.1](https://huggingface.co/datasets/jondurbin/airoboros-2.1)
- [alpaca-gpt4](https://huggingface.co/datasets/vicgalle/alpaca-gpt4)
- [dolphin](https://huggingface.co/datasets/cognitivecomputations/dolphin) - Only GPT-4 responses (flan1m-alpaca-uncensored-deduped.jsonl)
- [open-platypus](https://huggingface.co/datasets/garage-bAInd/Open-Platypus)
- [orca_mini_v1](https://huggingface.co/datasets/pankajmathur/orca_mini_v1_dataset)
- [SlimOrca-Dedup](https://huggingface.co/datasets/Open-Orca/SlimOrca-Dedup)
- [Synthia-1.3](https://huggingface.co/datasets/migtissera/Synthia-v1.3)
- [wizard_alpaca_dolly_orca](https://huggingface.co/datasets/nRuaif/wizard_alpaca_dolly_orca)
#### Conversation Score Prompt (Modified)
- [Capybara](https://huggingface.co/datasets/LDJnr/Capybara)
- [ultrachat](https://huggingface.co/datasets/HuggingFaceH4/ultrachat_200k)
## Score Breakdown (Needs to be updated)
| Dataset                 |         5 |         4 |         3 |         2 |         1 |         0 |
|-------------------------|----------:|----------:|----------:|----------:|----------:|----------:|
| dolphin                 | 80.232373 | 10.841314 |  2.217159 |  3.075088 |  3.63371  |  0.000356 |
| open-platypus           | 76.390115 | 10.779909 |  3.093156 |  3.558533 |  6.178288 |  0        |
| Capybara                | 73.57241  | 12.851431 |  3.005123 |  4.117206 |  6.435087 |  0.018743 |
| airoboros-2.1           | 69.869994 | 26.695312 |  1.322096 |  1.076957 |  1.035641 |  0        |
| alpaca-gpt4             | 65.421891 | 31.797554 |  1.301823 |  0.824937 |  0.653796 |  0        |
| wizard_alpaca_dolly_orca| 63.898674 | 32.68317  |  1.752752 |  0.894614 |  0.769829 |  0.00096  |
| ultrachat               | 50.213948 | 40.684169 |  5.741387 |  2.880979 |  0.478934 |  0.000582 |
| orca_mini_v1            | 46.351518 | 49.313846 |  1.568606 |  1.898745 |  0.867284 |  0        |
| Synthia-v1.3            | 39.262214 | 52.335033 |  2.627859 |  3.38096  |  2.392252 |  0.001683 |
| SlimOrca-Dedup          | 29.987262 | 55.132314 |  7.122872 |  2.998424 |  4.759127 |  0        |

## Prompts (Need to be updated)
#### Original Score Prompt from paper
```
Below is an instruction from an user and a candidate answer. Evaluate whether or not the answer is a good example of how AI Assistant should respond to the user’s instruction. Please assign a score using the following 5-point scale:
1: It means the answer is incomplete, vague, off-topic, controversial, or not exactly what the user asked for. For example, some content seems missing, numbered list does not start from the beginning, the opening sentence repeats user’s question. Or the response is from another person’s perspective with their personal experience (e.g. taken from blog posts), or looks like an answer from a forum. Or it contains promotional text, navigation text, or other irrelevant information.
2: It means the answer addresses most of the asks from the user. It does not directly address the user’s question. For example, it only provides a high-level methodology instead of the exact solution to user’s question.
3: It means the answer is helpful but not written by an AI Assistant. It addresses all the basic asks from the user. It is complete and self contained with the drawback that the response is not written from an AI assistant’s perspective, but from other people’s perspective. The content looks like an excerpt from a blog post, web page, or web search results. For example, it contains personal experience or opinion, mentions comments section, or share on social media, etc.
4: It means the answer is written from an AI assistant’s perspective with a clear focus of addressing the instruction. It provide a complete, clear, and comprehensive response to user’s question or instruction without missing or irrelevant information. It is well organized, self-contained, and written in a helpful tone. It has minor room for improvement, e.g. more concise and focused.
5: It means it is a perfect answer from an AI Assistant. It has a clear focus on being a helpful AI Assistant, where the response looks like intentionally written to address the user’s question or instruction without any irrelevant sentences. The answer provides high quality content, demonstrating expert knowledge in the area, is very well written, logical, easy-to-follow, engaging and insightful.
Please first provide a chain of thought brief reasoning you used to derive the rating score, and
then write "Score: <rating>" in the last line.
```
#### Conversation Score Prompt (Modified)
```
Below are a series of user instructions and corresponding candidate answers in a multi-turn conversation. Evaluate whether or not each answer is a good example of how the AI Assistant should respond to the user’s instructions in the context of an ongoing dialogue. Please assign a score using the following 5-point scale:
1: The answer is incomplete, vague, off-topic, controversial, or fails to build upon previous turns in the conversation. It might ignore context provided earlier, repeat information unnecessarily, or deviate from the conversational flow. Examples include missing content that should logically follow from earlier turns, responses that reset the conversation without acknowledging past interactions, or introducing irrelevant or promotional information.
2: The answer addresses the user's concerns but misses key elements of context or nuance from previous turns. It might provide a generally correct direction but fails to leverage the multi-turn nature of the conversation, such as not recalling information provided earlier or not sufficiently building upon it.
3: The answer is helpful and acknowledges the multi-turn context but reads more like a series of standalone responses rather than a cohesive conversation. It covers the basic asks from the user across multiple turns but might lack a seamless integration of conversation history or a sense of ongoing dialogue.
4: The answer is well-tailored to a multi-turn conversation, showing awareness of previous interactions and building upon them effectively. It is clear, comprehensive, and maintains a conversational flow, with only minor room for improvement, such as refining the integration of past and current turns or enhancing conversational fluidity.
5: The answer exemplifies perfect handling of a multi-turn conversation by an AI Assistant. It seamlessly integrates information from previous turns, providing high-quality, context-aware responses that demonstrate expert knowledge and maintain a logical, engaging, and insightful dialogue flow throughout.
Please first provide a brief chain of thought reasoning you used to derive the rating score, considering how well the AI Assistant maintains and builds upon the conversational context. Then write "Score: <rating>" in the last line.
```
