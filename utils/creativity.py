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

def read_prompt_subcategory(eval_set, category):
    cate_name = category.lower().replace(' ','_')
    filepath = os.path.join("../prompts", f"{eval_set}/{cate_name}.txt")
    with open(filepath, 'r') as file:
        return file.read()

def qwenmax_infer_instance(question, pred, category, qwenmax):
    system_prompt = read_prompt_subcategory('creativity', category)
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
