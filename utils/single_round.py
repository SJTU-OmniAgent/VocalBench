import sys
import json 
import random 
import os 
import re
import argparse
import random
import time
from config import keys, Qwen_Max

random.seed(int(time.time()))
os.environ["QWEN_API_KEY"] = random.choice(keys)
sys.path.append("./")


def qwenmax_infer_instance(question, pred, category, qwenmax):
    system_prompt = '''
You are now an evaluator. You will be given a question that asks for practical advice or guidance, along with the model-generated response. Your task is to evaluate the response using a 5-point scale based on how helpful, accurate, complete, and relevant the advice is to the question.

Grading Criteria
5 points: Excellent. The response provides clear, detailed, and highly relevant advice that directly addresses the question. It includes valuable steps or insights, is logically organized, and fully meets the user's needs.
4 points: Good. The response offers useful advice that is mostly relevant and well-structured. There may be minor omissions or slight lack of detail, but overall it is helpful and on-topic.
3 points: Medium. The response attempts to give advice and covers the basic aspects of the question, but lacks depth, specificity, or clarity. Some parts may be vague or overly general, limiting its usefulness.
2 points: Weak. The advice is incomplete, off-topic, or too vague to be useful. It may only partially address the question or contain significant gaps in logic or relevance.
1 point: Poor. The response fails to provide any meaningful or usable advice. It is irrelevant, misleading, or shows little understanding of the question being asked.

Output Format
Provide a brief explanation of your evaluation followed by the final score in square brackets. Use this exact format:

The response gives clear and actionable steps that directly answer the question, though one suggestion could be more specific. Score: [4]
    '''
    user_content = f"Question: {question}\n\n  Response: {pred}"
    for i in range(10):
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_content
            }
        ]
        text = qwenmax(messages)["text"]
        try:
            score = int(re.findall(r'\[([0-5])\]', text)[0])
            return score, text
        except:
            score = 1  
    return score, text


def qwenmax_eval_json(input_json, output_json):
    eval_data = []
    finished_len = 0
    total_score = 0

    if os.path.exists(output_json):
        with open(output_json, "r") as f:
            finished = json.load(f)
        for item in finished:
            eval_data.append(item)
            total_score += item["Score"]
        finished_len = len(finished)

    with open("../json/creativity.json", "r") as f:
        metadata = json.load(f)

    with open(input_json, "r") as f:
        data = json.load(f)
    
    qwenmax = Qwen_Max(model_name="qwen-max-2025-01-25")
    for instance in data[finished_len:]:
        response = instance["Response"]
        index = int(instance["Qid"].split('-')[-1])
        question = metadata[index]["Question"]
        category = metadata[index]["Category"]


        score, explain = qwenmax_infer_instance(question, response, category, qwenmax)
        eval_data.append({
            "Qid": instance["Qid"],
            "Question": question,
            "Response": instance["response"],
            "Score": score,
            "Explain": explain
        })
        total_score += score
        
        with open(output_json, 'w+', encoding='utf-8') as f:
            json.dump(eval_data, f, ensure_ascii=False, indent=4)
            
    print(f"Average Score: {total_score/(len(eval_data))}")


if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_json", type=str)
    parser.add_argument("--output_json", type=str)
    args = parser.parse_args()
    
    qwenmax_eval_json(args.input_json, args.output_json)
