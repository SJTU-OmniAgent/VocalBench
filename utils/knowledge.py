import json
import sys
import argparse
import re
from whisper_asr.whisper_normalizer.english import EnglishTextNormalizer

sys.path.append("./")

def remove_sp(text):
    gt = re.sub(r"<\|.*?\|>", " ", text)
    gt = re.sub(rf"\s+", r" ", gt)
    gt = re.sub(f" ?([!,.?;:])", r"\1", gt)
    gt = re.sub(r"-", " ", gt)
    gt = gt.lstrip(" ")
    return gt

def eval_knowledge(input_json, output_json):
    english_normalizer = EnglishTextNormalizer()
    ref_json = '../json/knowledge.json'
    with open(ref_json, "r", encoding = 'utf-8') as f:
        ref = json.load(f)
    with open(input_json, "r", encoding = 'utf-8') as f:
        try:
            data = json.load(f)
        except:
            f.seek(0)
            data = [json.loads(line) for line in f]
    correct_num = 0
    correct_num_s2s = 0

    for instance in data:
      index = int(instance['Qid'].split('-')[1])
      ans = english_normalizer(remove_sp(ref[index]["Answer"])).lower()
      response = english_normalizer(remove_sp(instance['Response'])).lower()
      response_s2s = english_normalizer(remove_sp(instance['Response_hyp'])).lower()
      if ans in response:
        correct_num += 1
      if ans in response_s2s:
        correct_num_s2s += 1
    print(f"S2T Accuracy: {correct_num/len(data)*100}%; S2S Accuracy: {correct_num_s2s/len(data)*100}%")

if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_json", type=str)
    args = parser.parse_args()
    eval_knowledge(args.input_json, args.output_json)
