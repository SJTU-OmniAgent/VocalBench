import os 
import requests

keys = ["YOUR_QWEN_KEY_1",
        "YOUR_QWEN_KEY_2",
        "YOUR_QWEN_KEY_3"]

EMOTION2VEC_PLUS_LARGE = '/workspace/tools/emotion2vec_plus_large'
WHISPER_LARGE_V3 = '/workspace/tools/whisper'

class Qwen_Max(object):
    def __init__(self, model_name="qwen-max-2025-01-25", temperature=0) -> None:
        self.model_name = model_name
        self.base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        self.url = f"{self.base_url}/chat/completions"
        self.api_key = os.getenv("QWEN_API_KEY")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        self.temperature = temperature

        
    def convert_to_qwen_format_messages(self, messages):
        new_messages = [{"role": "system", "content": "You are a helpful assistant."}]
        for message in messages:
            assert message["role"] in ["user", "system", "assistant"]
            if isinstance(message["content"], str):
                new_messages.append({"role": message["role"], "content": message["content"]})
            elif isinstance(message["content"], list):
                new_messages.append({"role": message["role"], "content": message["content"][0]['text']})
            else:
                raise ValueError("message content must be str or list as standard message format")
        return new_messages
    
    def __call__(self, messages, retry=10):
        if isinstance(messages, str):
            messages = [{"role": "system", "content": "You are a helpful assistant."}, {"role":"user","content": messages}]
        elif isinstance(messages, list):
            if len(messages) > 0 and isinstance(messages[0]["content"], list):
                messages = self.convert_to_qwen_format_messages(messages)
        else:
            raise ValueError("message content must be str or list as standard message format")
        
        data = {
            "model": "qwen-max-2025-01-25",  
            "messages": messages,
            "temperature": self.temperature,
        }

        i = 0
        while i < retry:
            response = requests.post(self.url, headers=self.headers, json=data, verify=False)

            if response.status_code == 200:
                result = response.json()
                txt_result = result["choices"][0]["message"]["content"]
                return {"text": txt_result}
            else:
                print(f"请求失败，状态码：{response.status_code}")
                print(response.text)
                i += 1
        else:
            return None 
