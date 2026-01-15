import json
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

def qwenmax_eval_emotion_semantic(question, question_emo, response, qwenmax):
    system_prompt = '''
You are now an emotional intelligence evaluator. You will be given a user question that contains clear emotional content, along with its associated emotion label, and a model-generated response. Your task is to evaluate how well the model's reply addresses the emotional tone of the question, shows understanding, and provides appropriate emotional support or positivity.

Grading Criteria
5 points: Excellent. The response fully acknowledges the emotional state of the user with clear empathy. It provides thoughtful, supportive, and emotionally uplifting feedback while remaining authentic and respectful.
4 points: Good. The response recognizes the user's emotions and offers appropriate support or encouragement. There may be slight gaps in depth or tone, but it remains emotionally intelligent and relevant.
3 points: Medium. The response attempts to acknowledge the user's feelings but does so in a somewhat generic or surface-level way. It may lack depth or miss subtle emotional cues, but still conveys basic empathy.
2 points: Weak. The response shows limited awareness of the emotional content. It may be overly dismissive, formulaic, or fail to provide meaningful emotional support. Tone might feel inappropriate or detached.
1 point: Poor. The response completely fails to recognize or address the emotional context. It may be cold, irrelevant, or even unintentionally insensitive.

Additional Notes
Focus on emotional resonance and tone, not grammar or spelling unless they significantly impair comprehension.
Consider whether the model validates the user's feelings and provides positive emotional value without being overly sentimental or fake.
Interpret the response generously—if the core emotional intent is clear, minor missteps shouldn't heavily penalize the score.

Output Format
Provide a brief explanation of your evaluation followed by the final score in square brackets. Use this exact format:

The response shows genuine understanding of the user's anxiety and offers comforting reassurance, though one phrase feels slightly overgeneralized. Score: [4]
  '''
    for i in range(10):
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"Question: {question}\n\n  Question Emotion: {question_emo}\n\n  Response: {response}"
            }
        ]
        print(messages)
        text = qwenmax(messages)["text"]
        try:
            score = int(re.findall(r'\[([0-5])\]', text)[0])
            return score, text
        except:
            score = 1
    return score, text

def part_correct(ans_zh, response):
  assert '·' in ans_zh
  answer_parts = ans_zh.split('·')
  for part in answer_parts:
      if part.strip() in response:  
          return True
  return False

def qwenmax_eval_json(input_json, output_json):
    ref_json = '../json/emotion.json'
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
        total_score += instance['Semantic_score']

    qwenmax = Qwen_Max(model_name="qwen-max-2025-01-25")
    
    for instance in data[len(instances):]:
      index = int(instance['Qid'].split('-')[1])
      response = instance['Response']
      question = ref[index]['Question']
      question_emo = ref[index]['Question_emo']
      score, explain = qwenmax_eval_emotion_semantic(question, question_emo, response, qwenmax)
      instances.append({
          'Qid': instance['Qid'],
          "Question": question,
          "Question_emo": question_emo,
          'Response': response,
          'Semantic_score': score,
          'Explain': explain
      })
      total_score += score

      with open(output_json, 'w+', encoding = 'utf-8') as outf:
        json.dump(instances, outf, ensure_ascii=False, indent = 4)
      
    print(f"Average Semantic Score: {total_score/len(instances)}")


if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_json", type=str)
    parser.add_argument("--output_json", type=str)
    args = parser.parse_args()
    qwenmax_eval_json(args.input_json, args.output_json)
