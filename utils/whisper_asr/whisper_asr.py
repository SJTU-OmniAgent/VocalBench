import os
import json
import re
from collections import defaultdict
import editdistance as ed
from evaluate_tokenizer import EvaluationTokenizer
from whisper_normalizer.english import EnglishTextNormalizer
from whisper_normalizer.basic import BasicTextNormalizer
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import soundfile as sf 
import json
import os 
import numpy as np
import argparse
import sys
import librosa
from shutil import copyfile

def load_whisper():
    local_model_path = "../tools/whisper" 
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        local_model_path, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    )
    model.to(device)
    processor = AutoProcessor.from_pretrained(local_model_path)
    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        torch_dtype=torch_dtype,
        device=device,
    )
    return pipe


def remove_sp(text, language):
    gt = re.sub(r"<\|.*?\|>", " ", text)
    gt = re.sub(rf"\s+", r" ", gt)
    gt = re.sub(f" ?([!,.?;:])", r"\1", gt)
    gt = re.sub(r"-", " ", gt)
    gt = gt.lstrip(" ")
    if language == "zh":
        gt = re.sub(rf"\s+", r"", gt)
    return gt

def whisper_asr(input_json, output_json, wav_dir):
    language = 'en'
    asr_pipe = load_whisper()
    english_normalizer = EnglishTextNormalizer()
    with open(input_json, 'r', encoding='utf-8') as infile:
      data = [json.loads(line) for line in infile]
    
    instances = []
    for index, item in enumerate(data):
        qid = item['Qid']
        wav_path = os.path.join(wav_dir, f"{qid}.wav")
        if os.path.exists(wav_path):
          audio_input, sample_rate = sf.read(wav_path)
          sample = {"raw": audio_input, "sampling_rate": sample_rate}
          result = asr_pipe(sample)
          response_hyp = english_normalizer(remove_sp(result["text"], language))
          print(asr_pred)
          instances.append({
            "Qid": item['Qid'],
            "Response": item['Response'],
            "Response_hyp": response_hyp
          })
    with open(output_json, 'w+', encoding='utf-8') as f:
      json.dump(instances, f, ensure_ascii=False, indent=4)


if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_json", type=str)
    parser.add_argument("--output_json", type=str)
    parser.add_argument("--audio_dir", type=str)
    args = parser.parse_args()
    whisper_asr(args.input_json, args.output_json, args.audio_dir)
