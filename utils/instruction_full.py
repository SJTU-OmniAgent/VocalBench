import json 
import os 
import argparse
import editdistance as ed
from funasr import AutoModel
from pydub import AudioSegment
import warnings
from whisper_asr.evaluate_tokenizer import EvaluationTokenizer
from whisper_asr.whisper_normalizer.english import EnglishTextNormalizer
from config import EMOTION2VEC_PLUS_LARGE

warnings.filterwarnings("ignore")
english_normalizer = EnglishTextNormalizer()

def compute_wer(refs, hyps, language):
    distance = 0
    ref_length = 0
    tokenizer = EvaluationTokenizer(
        tokenizer_type="none",
        lowercase=True,
        punctuation_removal=True,
        character_tokenization=False,
    )
    for i in range(len(refs)):
        ref = refs[i]
        pred = hyps[i]
        if language in ["en"]:
            ref = english_normalizer(ref)
            pred = english_normalizer(pred)
        ref_items = tokenizer.tokenize(ref).split()
        pred_items = tokenizer.tokenize(pred).split()
        distance += ed.eval(ref_items, pred_items)
        ref_length += len(ref_items)
        
    return distance, ref_length

def find_emotion_id(text):
    id2emotion = ['angry', 'happy', 'neutral', 'sad', 'surprised', 'unknown']
    return id2emotion.index(text) 

def get_audio_duration(file_path):
    audio = AudioSegment.from_file(file_path)
    duration = len(audio) 
    return duration

def count_words(text):
    return len(text.strip().split())

def gen_score(eval_json):
    wav_dir = eval_json.replace('result/instruction_following.json', 'wav/instruction_following')
    query_dir = '../audio/instruction_following'
    emotion_model = AutoModel(
          model=EMOTION2VEC_PLUS_LARGE,
          hub="ms",  
    )

    sucess = 0
    with open(eval_json, "r") as f:
        data = json.load(f)
    num = len(data)

    ref_json = '../json/instruction_following.json'
    with open(ref_json, "r", encoding = 'utf-8') as f:
        ref = json.load(f)

    asr_json = eval_json.replace('_semantic', '').replace('result', 'json_asr')
    with open(asr_json, "r", encoding = 'utf-8') as f:
        asr = json.load(f)
    assert len(asr) == len(data)
    
    for id, instance in enumerate(data):
        instance['Success'] = False
        index = int(instance['Qid'].split('-')[1])
        wav_file = os.path.join(wav_dir, instance['Qid'] + '.wav')
        if os.path.exists(wav_file):
          if index < 200 and instance['Correct']:
            gt = instance["Response"].lower()
            hyp = asr[id]["Response_hyp"].lower()
            distance, ref_length = compute_wer([gt], [hyp], 'en')
            instance_wer = distance / ref_length if ref_length != 0 else 0.0
            if (instance_wer) < 0.2:
              if index < 50:
                  instance['Success'] = True
              elif index in range(50, 100):
                  emo_id = find_emotion_id(ref[index]['Text_emo'])
                  rec_result = emotion_model.generate(wav_file, output_dir="./save", granularity="utterance", extract_embedding=False)
                  prob_scores = rec_result[0]['scores'][emo_id]
                  if prob_scores > 0.5:
                    instance['Success'] = True
              elif index in range(100, 150):
                  all_len = count_words(instance["Question"])
                  valide_len = count_words(instance["Question"].split('.', 1)[1])
                  query_dur = get_audio_duration(os.path.join(query_dir, instance['Qid'].split('-')[1] + '.wav'))* valide_len / all_len
                  response_dur = get_audio_duration(wav_file) 
                  if "twice my speaking speed" in instance["Question"].lower():
                    min_dur = query_dur * 0.25
                    max_dur = query_dur * 0.75
                  elif "half my speaking speed" in instance["Question"].lower():
                    min_dur = query_dur * 1.5
                    max_dur = query_dur * 2.5
                  else:
                    raise ValueError("Unknown time scale")
                  if min_dur < response_dur < max_dur:
                    instance['Success'] = True
              elif index in range(150, 200):
                  emo_id = find_emotion_id(ref[index]['Text_emo'])
                  rec_result = emotion_model.generate(wav_file, output_dir="./from_yuhao", granularity="utterance", extract_embedding=False)
                  prob_scores = rec_result[0]['scores'][emo_id]
                  if prob_scores > 0.5:
                    all_len = count_words(instance["Question"])
                    valide_len = count_words(instance["Question"].split('.', 1)[1])
                    query_dur = get_audio_duration(os.path.join(query_dir, instance['Qid'].split('-')[1] + '.wav'))* valide_len / all_len
                    response_dur = get_audio_duration(wav_file) 
                    if "twice my speaking speed" in instance["Question"].lower():
                      min_dur = query_dur * 0.25
                      max_dur = query_dur * 0.75
                    elif "half my speaking speed" in instance["Question"].lower():
                      min_dur = query_dur * 1.5
                      max_dur = query_dur * 2.5
                    else:
                      raise ValueError("Unknown time scale")
                    if min_dur < response_dur < max_dur:
                      instance['Success'] = True
          elif index>=200:
            instance['Success'] = instance["Correct"]
          sucess += instance['Success']
    print(f"Following Rate: {sucess/num*100}%.")

    output_json = eval_json.replace('.json', '_final.json')
    with open(output_json, 'w+', encoding = 'utf-8') as outf:
      json.dump(data, outf, ensure_ascii=False, indent = 4)
    
if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval_json", type=str)
    args = parser.parse_args()
    gen_score(args.eval_json)
