import time
import random
import json
import requests
import os
from datetime import datetime
from typing import List, Dict
from api_client import XiaomimimoAPIClient
from user_simulator import UserSimulator
from scenarios import SCENARIOS, get_random_scenario
from logger import logger


class DualAIConversation:
    def __init__(self, api_client: XiaomimimoAPIClient):
        self.api_client = api_client
        self.user_simulator = UserSimulator(error_rate=0.12)
        self.conversation_history: List[Dict] = []
        self.max_tokens = 2000

    def generate_user_message(self, scenario: dict, is_first: bool = False) -> str:
        if is_first:
            user_prompt = scenario["user_prompt"]
            return self.user_simulator.simulate_user_response(user_prompt)
        
        if self.user_simulator.detect_topic_stagnation(self.conversation_history):
            topic_change_msg = self.user_simulator.generate_topic_change_message(scenario)
            return self.user_simulator.simulate_user_response(topic_change_msg)
        
        user_messages = [msg for msg in self.conversation_history if msg["role"] == "user"]
        followup_index = len(user_messages) % len(scenario["user_followups"])
        followup = scenario["user_followups"][followup_index]
        
        context = self._get_conversation_context(last_n=3)
        
        context_prompt = f"""基于以下对话上下文，作为用户继续提问或回应。你的回答应该自然、真实，偶尔有语法问题或错别字。

上下文：
{context}

请继续对话，从以下角度选择一个回应：
1. 提出新的问题
2. 请求进一步解释
3. 表达困惑或理解
4. 感谢或结束对话

回应（简短自然，1-2句话）："""
        
        try:
            messages = [
                {"role": "system", "content": "你是一个普通用户，偶尔会有语法问题和错别字。回答要简短自然。"},
                {"role": "user", "content": context_prompt}
            ]
            
            response = self.api_client.chat_completion(
                messages=messages,
                temperature=0.8,
                max_tokens=200
            )
            
            user_message = response["choices"][0]["message"]["content"].strip()
            return self.user_simulator.simulate_user_response(user_message)
        except (requests.RequestException, KeyError, IndexError, json.JSONDecodeError) as e:
            logger.warning(f"生成用户消息失败，使用备用followup: {e}")
            return self.user_simulator.simulate_user_response(followup)

    def generate_ai_response(self, user_message: str, scenario: dict) -> str:
        context = self._get_conversation_context(last_n=3)
        
        messages = [
            {"role": "system", "content": scenario["ai_role"]},
            {"role": "user", "content": context},
            {"role": "user", "content": user_message}
        ]
        
        ai_response = ""
        print(f"\n🤖 AI助手: ", end="", flush=True)
        
        for chunk in self.api_client.chat_completion_stream(
            messages=messages,
            temperature=0.7,
            max_tokens=self.max_tokens
        ):
            if "choices" in chunk and len(chunk["choices"]) > 0:
                delta = chunk["choices"][0].get("delta", {})
                content = delta.get("content", "")
                if content:
                    print(content, end="", flush=True)
                    ai_response += content
        
        print()
        return ai_response

    def _get_conversation_context(self, last_n: int = 3) -> str:
        recent_messages = self.conversation_history[-last_n:]
        context_parts = []
        for msg in recent_messages:
            role = "用户" if msg["role"] == "user" else "AI助手"
            context_parts.append(f"{role}: {msg['content']}")
        return "\n".join(context_parts)

    def run_conversation(self, num_rounds: int = None) -> List[Dict]:
        if num_rounds is None:
            num_rounds = random.randint(30, 100)
        
        scenario = get_random_scenario()
        logger.info(f"场景: {scenario['name']}, 描述: {scenario['description']}, 轮数: {num_rounds}")
        
        self.conversation_history = []
        
        for round_num in range(1, num_rounds + 1):
            logger.info(f"第 {round_num} 轮对话")
            
            is_first = round_num == 1
            
            user_message = self.generate_user_message(scenario, is_first)
            self.conversation_history.append({"role": "user", "content": user_message})
            
            print(f"\n👤 用户: {user_message}")
            
            ai_response = self.generate_ai_response(user_message, scenario)
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            time.sleep(0.3)
        
        return self.conversation_history, scenario

    def save_conversation(self, conversation: List[Dict], scenario: dict, output_dir: str = "./conversations"):
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        scenario_name = scenario['name']
        filename = f"{scenario_name}_{timestamp}.json"
        output_path = os.path.join(output_dir, filename)
        
        output_data = {
            "scenario": scenario,
            "conversation": conversation,
            "total_rounds": len([m for m in conversation if m["role"] == "user"]),
            "created_at": datetime.now().isoformat()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"对话已保存到: {output_path}")
        return output_path
