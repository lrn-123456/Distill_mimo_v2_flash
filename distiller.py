import json
import time
from typing import List, Dict, Optional
from pathlib import Path
from api_client import XiaomimimoAPIClient
from conversation_splitter import ConversationSplitter
from logger import logger


class ConversationDistiller:
    def __init__(self, api_client: XiaomimimoAPIClient, splitter: ConversationSplitter):
        self.api_client = api_client
        self.splitter = splitter
        self.distillation_prompt = """你是一个对话蒸馏专家。请仔细阅读以下长对话内容，然后提炼出其中的核心信息、关键观点和重要结论。

要求：
1. 保留对话的主要脉络和逻辑结构
2. 提炼关键问题和答案
3. 保留重要的技术细节和参数
4. 简化冗余的对话内容
5. 使用简洁清晰的语言重新组织

请以结构化的方式输出蒸馏结果，包含以下部分：
- 对话主题
- 核心问题
- 关键观点
- 重要结论
- 相关技术细节

对话内容：
{conversation_content}

蒸馏结果："""

    def distill_conversation(self, messages: List[Dict], output_path: Optional[str] = None) -> Dict:
        if not messages:
            raise ValueError("对话消息列表不能为空")
        
        last_message = messages[-1]
        if last_message.get("role") != "assistant":
            logger.warning("对话不以AI回答结尾，将移除最后一条用户消息")
            messages = [msg for msg in messages if msg.get("role") == "assistant"]
            if not messages:
                raise ValueError("对话中没有任何AI回答")
        
        chunks = self.splitter.split_conversation(messages, method="tokens")
        
        distilled_results = []
        for idx, chunk in enumerate(chunks):
            logger.info(f"正在蒸馏第 {idx + 1}/{len(chunks)} 个片段...")
            
            conversation_text = self._format_conversation(chunk)
            
            try:
                result = self._call_distillation_api(conversation_text)
                distilled_results.append({
                    "chunk_index": idx,
                    "original_messages": chunk,
                    "distilled_content": result
                })
                time.sleep(0.5)
            except Exception as e:
                logger.error(f"蒸馏第 {idx + 1} 个片段时出错: {e}")
                distilled_results.append({
                    "chunk_index": idx,
                    "original_messages": chunk,
                    "distilled_content": None,
                    "error": str(e)
                })

        final_summary = self._generate_final_summary(distilled_results)
        
        output = {
            "total_chunks": len(chunks),
            "distilled_chunks": distilled_results,
            "final_summary": final_summary
        }

        if output_path:
            self._save_output(output, output_path)

        return output

    def _format_conversation(self, messages: List[Dict]) -> str:
        formatted = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            formatted.append(f"{role.upper()}: {content}")
        return "\n\n".join(formatted)

    def _call_distillation_api(self, conversation_text: str) -> str:
        prompt = self.distillation_prompt.format(conversation_content=conversation_text)
        
        messages = [
            {"role": "system", "content": "你是一个专业的对话蒸馏助手，擅长提炼长对话的核心信息。"},
            {"role": "user", "content": prompt}
        ]
        
        response = self.api_client.chat_completion(
            messages=messages,
            temperature=0.3,
            max_tokens=2000
        )
        
        return response["choices"][0]["message"]["content"]

    def _generate_final_summary(self, distilled_results: List[Dict]) -> str:
        successful_results = [r for r in distilled_results if r.get("distilled_content")]
        
        if not successful_results:
            return "无法生成最终摘要，所有片段蒸馏均失败。"

        all_distilled = "\n\n".join([
            f"片段 {r['chunk_index'] + 1}:\n{r['distilled_content']}"
            for r in successful_results
        ])

        summary_prompt = f"""请将以下多个对话片段的蒸馏结果整合成一个完整的、连贯的摘要。

蒸馏片段：
{all_distilled}

请生成一个完整的对话摘要，包含：
1. 整体对话主题
2. 主要讨论的问题
3. 核心观点和结论
4. 重要技术细节

完整摘要："""

        try:
            messages = [
                {"role": "system", "content": "你是一个专业的对话摘要助手，擅长整合多个信息源。"},
                {"role": "user", "content": summary_prompt}
            ]
            
            response = self.api_client.chat_completion(
                messages=messages,
                temperature=0.3,
                max_tokens=3000
            )
            
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"生成最终摘要时出错: {e}")
            return "生成最终摘要失败，但各片段蒸馏结果已保存。"

    def _save_output(self, output: Dict, output_path: str):
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        logger.info(f"蒸馏结果已保存到: {output_path}")

    def distill_conversation_file(self, input_path: str, output_path: str) -> Dict:
        with open(input_path, 'r', encoding='utf-8') as f:
            messages = json.load(f)
        
        return self.distill_conversation(messages, output_path)

    def batch_distill(self, input_dir: str, output_dir: str):
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        json_files = list(input_path.glob("*.json"))
        
        logger.info(f"找到 {len(json_files)} 个对话文件待处理")

        for idx, json_file in enumerate(json_files):
            logger.info(f"处理文件 {idx + 1}/{len(json_files)}: {json_file.name}")
            
            output_file = output_path / f"distilled_{json_file.name}"
            
            try:
                self.distill_conversation_file(str(json_file), str(output_file))
            except Exception as e:
                logger.error(f"处理文件 {json_file.name} 时出错: {e}")
