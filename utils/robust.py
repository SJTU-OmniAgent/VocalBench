import json
import sys
import random 
import os 
import re
import argparse
import time
from collections import defaultdict
from config import keys, Qwen_Max

random.seed(int(time.time()))
os.environ["QWEN_API_KEY"] = random.choice(keys)
sys.path.append("./")

def qwenmax_eval_robust(question, response, qwenmax):
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
    user_content = f"Question: {question}\n\n  Response: {response}"
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
    ref_json = '../json/robust_clean.json'
    with open(ref_json, "r", encoding = 'utf-8') as f:
        ref = json.load(f)
    with open(input_json, "r", encoding = 'utf-8') as f:
        try:
            data = json.load(f)
        except:
            f.seek(0)
            data = [json.loads(line) for line in f]
    
    instances = []
    total_score = 0
    if os.path.exists(output_json):
      with open(output_json, "r") as f:
        finished = json.load(f)
      for instance in finished:
        instances.append(instance)
        total_score += instance['Score']

    qwenmax = Qwen_Max(model_name="qwen-max-2025-01-25")
    
    for instance in data[len(instances):]:
      index = int(instance['Qid'].split('-')[-1])
      response = instance['Response']
      question = instance['Question']
      score, explain = qwenmax_eval_robust(question, response, qwenmax)
      total_score += score
      instances.append({
          'Qid': index,
          'Question': question,
          'Response': response,
          'Score': score,
          'Explain': explain
      })

      with open(output_json, 'w+', encoding = 'utf-8') as outf:
        json.dump(instances, outf, ensure_ascii=False, indent = 4)
      
def gen_score(output_json):
    assert output_json.endswith('robust.json')
    single_round_json = output_json.replace('robust.json', 'single_round.json')
    assert os.path.exists(single_round_json)
    with open(single_round_json, "r", encoding = 'utf-8') as f:
        sr_data = json.load(f)

    robust_clean_path = '../json/robust_clean.json'
    refer_path = '../json/single_round.json'
    with open(robust_clean_path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)
    with open(refer_path, 'r', encoding='utf-8') as f:
        refer_data = json.load(f)
    input_answers = {item['Answer'] for item in input_data}
    matched_qids = []
    for item in refer_data:
        if item['Answer'] in input_answers:
            matched_qids.append(item['Qid'])
    scores = []
    for item in sr_data:
        if item['Qid'] in matched_qids and 's2t_score' in item:
            scores.append(item['Score'])
    clean_score = sum(scores) / len(scores)

    with open(output_json, "r", encoding = 'utf-8') as f:
        data = json.load(f)
    
    set_scores = defaultdict(lambda: {'Score': []})
    for item in data:
        qid = item.get('Qid')
        score = item.get('Score')
        if not qid or score is None:
            continue  
        parts = qid.rsplit('-', 1)
        if len(parts) < 2:
            continue 
        set_name = parts[0]
        set_scores[set_name]['Score'].append(score)
    
    total_score = 0
    eval_sets = ['robust-background_noise-snr_-5', 'robust-white_noise-snr_-5', 'robust-reverberation-rt60_30', 'robust-packet_loss-dropping_0.70', 'robust-farfield-filter_400hz', 'robust-distortion-clipping_0.0001']
    for set_name in eval_sets:
        avg_score = sum(set_scores[set_name]['Score']) / len( set_scores[set_name]['Score']) if set_scores[set_name]['Score'] else 0
        pr = min(1, avg_score/clean_score)*2.5
        total_score = total_score + pr
    print(total_score/15 * 100)
    print(f"Robustness Preserve Rate: {total_score/15 * 100}%")

if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_json", type=str)
    parser.add_argument("--output_json", type=str)
    args = parser.parse_args()
    qwenmax_eval_json(args.input_json, args.output_json)
    gen_score(args.output_json)
