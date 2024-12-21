score_prompt_conversation = '''Below are a series of user instructions and corresponding candidate answers in a multi-turn conversation. Evaluate whether or not each answer is a good example of how the AI Assistant should respond to the user’s instructions in the context of an ongoing dialogue. Please assign a score using the following 5-point scale:
1: The answer is incomplete, vague, off-topic, controversial, or fails to build upon previous turns in the conversation. It might ignore context provided earlier, repeat information unnecessarily, or deviate from the conversational flow. Examples include missing content that should logically follow from earlier turns, responses that reset the conversation without acknowledging past interactions, or introducing irrelevant or promotional information.
2: The answer addresses the user's concerns but misses key elements of context or nuance from previous turns. It might provide a generally correct direction but fails to leverage the multi-turn nature of the conversation, such as not recalling information provided earlier or not sufficiently building upon it.
3: The answer is helpful and acknowledges the multi-turn context but reads more like a series of standalone responses rather than a cohesive conversation. It covers the basic asks from the user across multiple turns but might lack a seamless integration of conversation history or a sense of ongoing dialogue.
4: The answer is well-tailored to a multi-turn conversation, showing awareness of previous interactions and building upon them effectively. It is clear, comprehensive, and maintains a conversational flow, with only minor room for improvement, such as refining the integration of past and current turns or enhancing conversational fluidity.
5: The answer exemplifies perfect handling of a multi-turn conversation by an AI Assistant. It seamlessly integrates information from previous turns, providing high-quality, context-aware responses that demonstrate expert knowledge and maintain a logical, engaging, and insightful dialogue flow throughout.
Please provide a rating score for the instruction & candidate answer between the "```" tags below, and then write "Score: <rating>" in the last line. Respond only with an integer score.

```
{instruction}
```

Score:
'''

score_prompt_original = '''Below is an instruction from an user and a candidate answer. Evaluate whether or not the answer is a good example of how AI Assistant should respond to the user’s instruction. Please assign a score using the following 5-point scale:
1: It means the answer is incomplete, vague, off-topic, controversial, or not exactly what the user asked for. For example, some content seems missing, numbered list does not start from the beginning, the opening sentence repeats user’s question. Or the response is from another person’s perspective with their personal experience (e.g. taken from blog posts), or looks like an answer from a forum. Or it contains promotional text, navigation text, or other irrelevant information.
2: It means the answer addresses most of the asks from the user. It does not directly address the user’s question. For example, it only provides a high-level methodology instead of the exact solution to user’s question.
3: It means the answer is helpful but not written by an AI Assistant. It addresses all the basic asks from the user. It is complete and self contained with the drawback that the response is not written from an AI assistant’s perspective, but from other people’s perspective. The content looks like an excerpt from a blog post, web page, or web search results. For example, it contains personal experience or opinion, mentions comments section, or share on social media, etc.
4: It means the answer is written from an AI assistant’s perspective with a clear focus of addressing the instruction. It provide a complete, clear, and comprehensive response to user’s question or instruction without missing or irrelevant information. It is well organized, self-contained, and written in a helpful tone. It has minor room for improvement, e.g. more concise and focused.
5: It means it is a perfect answer from an AI Assistant. It has a clear focus on being a helpful AI Assistant, where the response looks like intentionally written to address the user’s question or instruction without any irrelevant sentences. The answer provides high quality content, demonstrating expert knowledge in the area, is very well written, logical, easy-to-follow, engaging and insightful.
Please provide a rating score for the instruction & candidate answer between the "```" tags below, and then write "Score: <rating>" in the last line. Respond only with an integer score.

```
{instruction}
```

Score:
'''

score_prompt_function_calling = '''Below is an instruction from a user involving a function call and the AI Assistant's response. Evaluate the response based on how accurately and effectively the AI Assistant utilized the function call to address the user's request. Use the following 5-point scale for your evaluation:

1: The response significantly misses the mark by failing to invoke the function call when required, using incorrect parameters, or providing an irrelevant, vague, or off-topic answer. It may also include inappropriate content not related to the function's output or the user's request.

2: The response makes an attempt to use the function call but does so inaccurately or incompletely. It addresses some aspects of the user's request but overlooks key parameters or misinterprets the function's intended use, leading to a partially correct or incomplete answer.

3: The response correctly invokes the function call and uses appropriate parameters but falls short in effectively communicating the function's output. The answer is functional and addresses the user's request but lacks clarity, detail, or may not fully leverage the function's response to provide a comprehensive answer.

4: The response demonstrates a good understanding of the function call, using it appropriately and accurately. It provides a clear and relevant answer to the user's request, with minor areas for improvement in terms of optimizing the explanation or presentation of the function's output.

5: The response exemplifies an ideal use of the function call, with perfect parameter interpretation and a precise, clear, and insightful explanation of the function's output. It fully addresses the user's request in a coherent, logical, and engaging manner, leaving no room for improvement.

Please provide a rating score for the provided example between the "```" tags below, following the criteria outlined above. Conclude your evaluation with "Score: <rating>", only using an integer between 1 and 5.

```
{instruction}
```
Score:
'''

score_prompt_agents = '''Below is a sequence of messages between an automated agent (ASSISTANT) and a user (Entrepreneur) within a simulated task scenario. Evaluate the automated agent's responses based on their effectiveness in addressing the user's needs, clarity of communication, appropriateness to the task at hand, and the agent's ability to creatively solve problems and guide the user towards their goal. Use the following 5-point scale for your evaluation:

1: The agent's responses are irrelevant or incorrect, lack clarity, fail to address the user's needs, or are inappropriate for the task at hand. The agent demonstrates poor problem-solving skills and fails to guide the user effectively.

2: The agent's responses attempt to address the user's needs but contain significant errors, lack clarity, or partially miss the task's requirements. The agent shows an attempt at problem-solving but falls short in creativity or effectiveness.

3: The agent's responses are adequate in addressing the user's needs, clear, and mostly appropriate for the task. The agent demonstrates good problem-solving skills but may lack creativity or fail to fully capitalize on opportunities to guide the user more effectively.

4: The agent's responses effectively address the user's needs, are clear and well-communicated, and are appropriate for the task at hand. The agent shows solid problem-solving skills and creativity, guiding the user towards their goal with minor areas for improvement.

5: The agent's responses exemplify an ideal interaction. They are highly effective in addressing the user's needs, exceptionally clear, and perfectly suited to the task. The agent demonstrates outstanding problem-solving skills and creativity, guiding the user towards their goal in the most efficient and helpful manner possible.

Please provide a rating score for the automated agent's responses within the "```" tags below, following the criteria outlined above. Conclude your evaluation with "Score: <rating>", using an integer between 1 and 5.

```
{instruction}
```

Score:
'''



score_prompt_coding = '''Below is a coding problem / query given to an AI Assistant and a candidate solution. Evaluate the solution based on its adherence to the problem statement, correctness, efficiency, and readability. Use the following 5-point scale for your evaluation:

1: The solution is incorrect or irrelevant to the problem statement. It may contain significant syntax errors, logical flaws, or be entirely off-topic. The code is difficult to understand and does not solve the given problem.

2: The solution attempts to address the problem but has major flaws in logic or efficiency. It may solve a part of the problem but fails to provide a complete solution. The code may be somewhat readable, but lacks proper structure or comments.

3: The solution correctly solves the problem but may not be optimal in terms of efficiency or coding practices. The code is generally readable and structured, but there may be room for improvement in terms of algorithmic efficiency, coding style, or documentation.

4: The solution provides a correct and efficient answer to the problem. The code is well-structured, readable, and follows good coding practices, with minor areas for improvement such as optimization or better documentation.

5: The solution exemplifies an ideal response to the coding problem. It is correct, efficient, and demonstrates deep understanding of algorithms and data structures. The code is highly readable, well-documented, and follows best coding practices without any apparent flaws.

Please provide a rating score for the provided coding related conversation between the "<|Coding Query|>" tags below, following the criteria outlined above. Conclude your evaluation with "Score: <rating>", using an integer between 1 and 5.

<|Coding Query|>
{instruction}
<|Coding Query|>

Score:
'''

score_prompt_sql = '''Below is an SQL query provided to the AI Assistant alongside a dataset description and the candidate's solution. Evaluate the solution based on its adherence to the query requirements, correctness of the output, efficiency of the query, and readability of the SQL code. Use the following 5-point scale for your evaluation:

1: The solution is incorrect or irrelevant to the query requirements. It may contain significant syntax errors, logical flaws, or fail to produce the correct dataset. The code is difficult to understand and does not solve the given problem.

2: The solution attempts to address the query but has major flaws in logic or efficiency. It may solve a part of the problem but fails to provide a complete or correct dataset. The code may be somewhat readable, but lacks proper structure or comments for clarity.

3: The solution correctly produces the requested dataset but may not be optimal in terms of query efficiency or database practices. The code is generally readable and structured, but there may be room for improvement in terms of execution efficiency, coding style, or documentation.

4: The solution provides a correct and efficient dataset according to the query. The SQL code is well-structured, readable, and follows good database practices, with minor areas for improvement such as further optimization or better documentation.

5: The solution exemplifies an ideal response to the SQL query. It is correct, efficient, and demonstrates deep understanding of database management and SQL optimization. The code is highly readable, well-documented, and adheres to best practices in database design and query formulation without any apparent flaws.

Please provide a rating score for the provided SQL query solution within the "<|SQL Query|>" tags below, following the criteria outlined above. Conclude your evaluation with "Score: <rating>", using an integer between 1 and 5.

```
{instruction}
```

Score:
''' 


score_prompt_math = '''Below is a mathematical problem provided to the AI Assistant and the candidate solution. Evaluate the solution based on its mathematical correctness, logical reasoning, clarity of explanation, and the model's ability to work through the problem systematically. Use the following 5-point scale for your evaluation:

1: The solution is incorrect or irrelevant, lacks logical reasoning, or fails to address the problem. The explanation is unclear, making the mathematical reasoning difficult to follow.

2: The solution attempts to address the problem but contains significant errors in mathematical reasoning or logic. The explanation may show an attempt at systematic reasoning but falls short in clarity or completeness.

3: The solution is mathematically correct but may not be the most efficient or elegant. The model demonstrates a good effort in reasoning through the problem, but the explanation could be more concise or better structured to aid understanding.

4: The solution is correct and demonstrates solid mathematical reasoning with a clear and logical progression of ideas. The explanation is clear, though there may be minor areas for improvement in terms of brevity or presentation.

5: The solution exemplifies an ideal mathematical explanation. It is correct, employs efficient and elegant reasoning, and the explanation is exceptionally clear and well-structured, making the solution easy to understand and follow.

Please provide a rating score for the provided mathematical solution between the "```" tags below, following the criteria outlined above. Conclude your evaluation with "Score: <rating>", using an integer between 1 and 5.

```
{instruction}
```

Score:
'''

score_prompt_science = '''Below is a scientific problem provided to the AI Assistant in the fields of physics, biology, or chemistry, along with the candidate's proposed solution. Evaluate the solution based on its scientific accuracy, logical reasoning, clarity of explanation, and the model's ability to approach the problem systematically. Use the following 5-point scale for your evaluation:

1: The solution is incorrect or irrelevant, lacks logical reasoning, or fails to address the problem accurately. The explanation is unclear, making the scientific reasoning difficult to follow.

2: The solution attempts to address the problem but contains significant errors in scientific reasoning or logic. The explanation may show an attempt at systematic reasoning but falls short in clarity or completeness.

3: The solution is scientifically accurate but may not be the most efficient, innovative, or thorough. The model demonstrates a good effort in reasoning through the problem, but the explanation could be more concise, detailed, or better structured to aid understanding.

4: The solution is correct and demonstrates solid scientific reasoning with a clear and logical progression of ideas. The explanation is clear, though there may be minor areas for improvement in terms of depth, brevity, or presentation.

5: The solution exemplifies an ideal scientific explanation. It is accurate, employs efficient and insightful reasoning, and the explanation is exceptionally clear and well-structured, making the solution easy to understand and follow.

Please provide a rating score for the provided scientific solution between the "```" tags below, following the criteria outlined above. Conclude your evaluation with "Score: <rating>", using an integer between 1 and 5.

```
{instruction}
```

Score:
'''

generate_rejected_pair_prompt = '''Belows are rules to evaluate whether or not the answer is a good example of how AI Assistant should respond to the user’s instruction. Please assign a score using the following 5-point scale:
1: It means the answer is incomplete, vague, off-topic, controversial, or not exactly what the user asked for. For example, some content seems missing, numbered list does not start from the beginning, the opening sentence repeats user’s question. Or the response is from another person’s perspective with their personal experience (e.g. taken from blog posts), or looks like an answer from a forum. Or it contains promotional text, navigation text, or other irrelevant information.
2: It means the answer addresses most of the asks from the user. It does not directly address the user’s question. For example, it only provides a high-level methodology instead of the exact solution to user’s question.
3: It means the answer is helpful but not written by an AI Assistant. It addresses all the basic asks from the user. It is complete and self contained with the drawback that the response is not written from an AI assistant’s perspective, but from other people’s perspective. The content looks like an excerpt from a blog post, web page, or web search results. For example, it contains personal experience or opinion, mentions comments section, or share on social media, etc.
4: It means the answer is written from an AI assistant’s perspective with a clear focus of addressing the instruction. It provide a complete, clear, and comprehensive response to user’s question or instruction without missing or irrelevant information. It is well organized, self-contained, and written in a helpful tone. It has minor room for improvement, e.g. more concise and focused.
5: It means it is a perfect answer from an AI Assistant. It has a clear focus on being a helpful AI Assistant, where the response looks like intentionally written to address the user’s question or instruction without any irrelevant sentences. The answer provides high quality content, demonstrating expert knowledge in the area, is very well written, logical, easy-to-follow, engaging and insightful.

TASK: “Generate only a response which you think represents score 2 (mostly), 1 with minimum 10 words based on the above rules for the prompt below the  <|prompt-start|> tag. Give only the response for the prompt below with minimum 10 words, donot start the response with "Score n:" or "n:", just give the final response.”

<|prompt-start|>
{instruction}

Here is the Score 2 (mostly), 1 Response:
'''

generate_accepted_pair_prompt = '''Belows are rules to evaluate whether or not the answer is a good example of how AI Assistant should respond to the user’s instruction. Please assign a score using the following 5-point scale:
1: It means the answer is incomplete, vague, off-topic, controversial, or not exactly what the user asked for. For example, some content seems missing, numbered list does not start from the beginning, the opening sentence repeats user’s question. Or the response is from another person’s perspective with their personal experience (e.g. taken from blog posts), or looks like an answer from a forum. Or it contains promotional text, navigation text, or other irrelevant information.
2: It means the answer addresses most of the asks from the user. It does not directly address the user’s question. For example, it only provides a high-level methodology instead of the exact solution to user’s question.
3: It means the answer is helpful but not written by an AI Assistant. It addresses all the basic asks from the user. It is complete and self contained with the drawback that the response is not written from an AI assistant’s perspective, but from other people’s perspective. The content looks like an excerpt from a blog post, web page, or web search results. For example, it contains personal experience or opinion, mentions comments section, or share on social media, etc.
4: It means the answer is written from an AI assistant’s perspective with a clear focus of addressing the instruction. It provide a complete, clear, and comprehensive response to user’s question or instruction without missing or irrelevant information. It is well organized, self-contained, and written in a helpful tone. It has minor room for improvement, e.g. more concise and focused.
5: It means it is a perfect answer from an AI Assistant. It has a clear focus on being a helpful AI Assistant, where the response looks like intentionally written to address the user’s question or instruction without any irrelevant sentences. The answer provides high quality content, demonstrating expert knowledge in the area, is very well written, logical, easy-to-follow, engaging and insightful.

TASK: “Generate only a response which you think represents score 5 based on the above rules for the prompt below the  <|prompt-start|> tag. Give the response only for the prompt below.”

<|prompt-start|>
{instruction}

Here is the Score 5 Response:
'''
