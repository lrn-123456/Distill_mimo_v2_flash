import re
from typing import List, Dict, Tuple
import tiktoken


class ConversationSplitter:
    def __init__(self, max_tokens: int = 4000, overlap_tokens: int = 200):
        self.max_tokens = max_tokens
        self.overlap_tokens = overlap_tokens
        self.encoding = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text: str) -> int:
        return len(self.encoding.encode(text))

    def split_conversation_by_turns(self, messages: List[Dict], max_turns: int = 10) -> List[List[Dict]]:
        chunks = []
        for i in range(0, len(messages), max_turns):
            chunk = messages[i:i + max_turns]
            if i > 0:
                overlap_messages = messages[max(0, i - 2):i]
                chunk = overlap_messages + chunk
            chunks.append(chunk)
        return chunks

    def split_conversation_by_tokens(self, messages: List[Dict]) -> List[List[Dict]]:
        chunks = []
        current_chunk = []
        current_tokens = 0

        for msg in messages:
            msg_tokens = self.count_tokens(msg.get("content", ""))
            
            if current_tokens + msg_tokens > self.max_tokens and current_chunk:
                chunks.append(current_chunk)
                current_chunk = []
                current_tokens = 0

            current_chunk.append(msg)
            current_tokens += msg_tokens

        if current_chunk:
            chunks.append(current_chunk)

        return self._add_overlap(chunks)

    def _add_overlap(self, chunks: List[List[Dict]]) -> List[List[Dict]]:
        if len(chunks) <= 1:
            return chunks

        overlapped_chunks = []
        overlapped_chunks.append(chunks[0])

        for i in range(1, len(chunks)):
            prev_chunk = chunks[i - 1]
            current_chunk = chunks[i]
            
            overlap_messages = []
            overlap_tokens = 0
            
            for msg in reversed(prev_chunk):
                msg_tokens = self.count_tokens(msg.get("content", ""))
                if overlap_tokens + msg_tokens <= self.overlap_tokens:
                    overlap_messages.insert(0, msg)
                    overlap_tokens += msg_tokens
                else:
                    break
            
            overlapped_chunk = overlap_messages + current_chunk
            overlapped_chunks.append(overlapped_chunk)

        return overlapped_chunks

    def split_long_message(self, message: Dict) -> List[Dict]:
        content = message.get("content", "")
        if self.count_tokens(content) <= self.max_tokens:
            return [message]

        chunks = []
        sentences = re.split(r'([。！？\n])', content)
        
        current_text = ""
        for i in range(0, len(sentences), 2):
            sentence = sentences[i]
            if i + 1 < len(sentences):
                sentence += sentences[i + 1]
            
            if self.count_tokens(current_text + sentence) > self.max_tokens and current_text:
                chunks.append({
                    "role": message["role"],
                    "content": current_text.strip()
                })
                current_text = sentence
            else:
                current_text += sentence

        if current_text:
            chunks.append({
                "role": message["role"],
                "content": current_text.strip()
            })

        return chunks

    def split_conversation(self, messages: List[Dict], method: str = "tokens") -> List[List[Dict]]:
        if method == "turns":
            return self.split_conversation_by_turns(messages)
        elif method == "tokens":
            return self.split_conversation_by_tokens(messages)
        else:
            raise ValueError(f"Unknown split method: {method}")
