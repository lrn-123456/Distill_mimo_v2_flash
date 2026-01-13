import requests
import json
from typing import List, Dict, Optional
from logger import logger


class XiaomimimoAPIClient:
    def __init__(self, api_key: str, base_url: str = "https://api.xiaomimimo.com/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def chat_completion(self, messages: List[Dict], model: str = "mimo-v2-flash", **kwargs) -> Dict:
        url = f"{self.base_url}/chat/completions"
        
        if "max_tokens" in kwargs:
            kwargs["max_completion_tokens"] = kwargs.pop("max_tokens")
        
        data = {
            "model": model,
            "messages": messages,
            **kwargs
        }
        try:
            response = requests.post(url, headers=self.headers, json=data, timeout=120)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"API请求失败: {e}")
            logger.error(f"响应内容: {response.text}")
            raise

    def chat_completion_stream(self, messages: List[Dict], model: str = "mimo-v2-flash", **kwargs):
        url = f"{self.base_url}/chat/completions"
        
        if "max_tokens" in kwargs:
            kwargs["max_completion_tokens"] = kwargs.pop("max_tokens")
        
        data = {
            "model": model,
            "messages": messages,
            "stream": True,
            **kwargs
        }
        response = requests.post(url, headers=self.headers, json=data, stream=True, timeout=120)
        response.raise_for_status()
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data_str = line[6:]
                    if data_str == '[DONE]':
                        break
                    try:
                        yield json.loads(data_str)
                    except json.JSONDecodeError:
                        continue

    def get_model_info(self) -> Dict:
        url = f"{self.base_url}/models"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
