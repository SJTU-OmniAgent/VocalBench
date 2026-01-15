import json
import argparse

def calc_acc(semantic_json, acoustic_json):
    with open(acoustic_json, 'r') as f:
        acoustic = json.load(f)
    with open(semantic_json, 'r') as f:
        semantic = json.load(f)
    
    assert len(acoustic) == len(semantic)
    semantic_acc = 0
    acoustic_acc = 0
    all_acc = 0
    for instance in acoustic:
      index = int(instance['Qid'].split('-')[1])
      if instance['Acoustic_score'] >= 3:
        acoustic_acc += 1
      if semantic[index].get('Semantic_score', 0) >= 3:
        semantic_acc += 1
      if instance['Acoustic_score'] >= 3 and semantic[index].get('Semantic_score', 0) >= 3:
        all_acc += 1
    print('Semantic EER: {:.1f}%'.format(semantic_acc / len(semantic)))
    print('Acoustic EER: {:.1f}%'.format(acoustic_acc / len(acoustic)))
    print('Final EER: {:.1f}%'.format(all_acc / len(acoustic)))

if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument("--semantic_json", type=str)
    parser.add_argument("--acoustic_json", type=str)
    args = parser.parse_args()    
    calc_acc(args.semantic_json, args.acoustic_json)
