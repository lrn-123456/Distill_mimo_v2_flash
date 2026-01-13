import random
from typing import List, Dict


class UserSimulator:
    def __init__(self, error_rate: float = 0.12):
        self.error_rate = error_rate
        self.common_typos = {
            "的": "得", "得": "的", "在": "再", "再": "在",
            "那": "哪", "哪": "那", "这里": "这", "那里": "那",
            "吗": "嘛", "呢": "呐", "啊": "呀",
            "知道": "道", "什么": "啥", "这个": "这个",
            "问题": "问题", "方法": "方法", "因为": "因为",
            "但是": "不过", "所以": "因此", "然后": "之后",
            "或者": "要么", "而且": "并且", "还有": "另外"
        }
        self.grammar_errors = [
            ("了", ""), ("的", "地"), ("地", "的"),
            ("是", "是是"), ("不", "不不"),
            ("很", "非常"), ("非常", "很"),
            ("一下", "一下下"), ("一下", ""),
            ("一下", "一下子"), ("一下", "一下儿")
        ]
        self.question_patterns = [
            "等等，我没太听懂",
            "不好意思，能再解释一下吗",
            "这个有点复杂诶",
            "等等，刚才说的那个是什么意思",
            "嗯？我没太明白",
            "那个，能举个具体的例子吗",
            "等等，这里有点晕",
            "不好意思打断一下",
            "等等，我想确认一下"
        ]
        self.doubt_patterns = [
            "真的吗？",
            "这样真的行吗",
            "我有点怀疑诶",
            "这个方法可靠吗",
            "会不会有问题啊",
            "我有点担心",
            "这样真的有效吗",
            "会不会太复杂了",
            "感觉不太对劲诶"
        ]
        self.emotion_expressions = [
            "哈哈", "哇", "厉害", "太棒了", "不错诶",
            "原来如此", "懂了懂了", "好的好的", "嗯嗯",
            "哦哦哦", "原来是这样", "好的好的", "嗯嗯嗯"
        ]
        self.repetition_patterns = [
            "等等，刚才说的那个再讲一遍？",
            "不好意思，刚才没太听清",
            "那个，能再说一遍吗",
            "等等，刚才那个是什么来着",
            "不好意思，能重复一下吗"
        ]

    def add_typos(self, text: str) -> str:
        if random.random() < self.error_rate:
            words = list(text)
            for i in range(len(words)):
                if words[i] in self.common_typos and random.random() < 0.25:
                    words[i] = self.common_typos[words[i]]
            text = ''.join(words)
        return text

    def add_grammar_errors(self, text: str) -> str:
        if random.random() < self.error_rate:
            for wrong, correct in self.grammar_errors:
                if random.random() < 0.15:
                    text = text.replace(wrong, correct)
        return text

    def add_informal_expressions(self, text: str) -> str:
        informal_map = {
            "不知道": "不太清楚", "为什么": "为啥",
            "怎么样": "咋样", "可以": "行不行",
            "好的": "ok", "谢谢": "谢啦",
            "不好意思": "那个", "请问": "那个",
            "明白了": "懂了", "理解": "明白"
        }
        for formal, informal in informal_map.items():
            if random.random() < 0.12:
                text = text.replace(formal, informal)
        return text

    def simulate_user_response(self, text: str) -> str:
        text = self.add_typos(text)
        text = self.add_grammar_errors(text)
        text = self.add_informal_expressions(text)
        text = self.add_human_behavior(text)
        return text

    def add_human_behavior(self, text: str) -> str:
        behavior_roll = random.random()
        
        if behavior_roll < 0.08:
            text = self.add_emotion_expression(text)
        elif behavior_roll < 0.16:
            text = self.add_question_pattern(text)
        elif behavior_roll < 0.24:
            text = self.add_doubt_pattern(text)
        elif behavior_roll < 0.32:
            text = self.add_repetition_pattern(text)
        elif behavior_roll < 0.40:
            text = self.add_thinking_pause(text)
        elif behavior_roll < 0.48:
            text = self.add_acknowledgment(text)
        
        return text

    def add_emotion_expression(self, text: str) -> str:
        expression = random.choice(self.emotion_expressions)
        return f"{expression}，{text}"

    def add_question_pattern(self, text: str) -> str:
        if random.random() < 0.5:
            pattern = random.choice(self.question_patterns)
            return f"{pattern}，{text}"
        return text

    def add_doubt_pattern(self, text: str) -> str:
        if random.random() < 0.6:
            pattern = random.choice(self.doubt_patterns)
            return f"{pattern}，{text}"
        return text

    def add_repetition_pattern(self, text: str) -> str:
        if random.random() < 0.4:
            pattern = random.choice(self.repetition_patterns)
            return f"{pattern}，{text}"
        return text

    def add_thinking_pause(self, text: str) -> str:
        pause_indicators = ["嗯...", "让我想想...", "那个...", "等等...", "哦...", "嗯嗯..."]
        if random.random() < 0.5:
            indicator = random.choice(pause_indicators)
            return f"{indicator}{text}"
        return text

    def add_acknowledgment(self, text: str) -> str:
        ack_phrases = ["好的好的", "嗯嗯", "哦哦", "原来如此", "懂了", "明白"]
        if random.random() < 0.5:
            phrase = random.choice(ack_phrases)
            return f"{phrase}，{text}"
        return text

    def detect_topic_stagnation(self, conversation_history: List[Dict], window_size: int = 4) -> bool:
        if len(conversation_history) < window_size * 2:
            return False
        
        recent_messages = conversation_history[-window_size:]
        
        user_messages = [msg["content"] for msg in recent_messages if msg["role"] == "user"]
        ai_messages = [msg["content"] for msg in recent_messages if msg["role"] == "assistant"]
        
        if len(user_messages) < 2 or len(ai_messages) < 2:
            return False
        
        last_user_msg = user_messages[-1] if user_messages else ""
        last_ai_msg = ai_messages[-1] if ai_messages else ""
        
        stagnation_indicators = [
            "好的", "知道了", "明白了", "谢谢", "晚安", "拜拜",
            "好的，谢谢", "好的，晚安", "好的，拜拜", "嗯嗯", "嗯",
            "好的，那我先", "那我先", "我去了", "我去试试", "我去试试看"
        ]
        
        for indicator in stagnation_indicators:
            if indicator in last_user_msg:
                return True
        
        if len(last_user_msg) < 10 and len(last_ai_msg) < 50:
            return True
        
        return False

    def generate_topic_change_message(self, scenario: dict) -> str:
        topic_change_phrases = [
            "对了，突然想到个问题",
            "说起来，我还想问问",
            "换个话题哈",
            "其实我还有个疑问",
            "顺便问一下",
            "话说回来",
            "对了",
            "那个",
            "我想了解下",
            "其实我想问"
        ]
        
        followups = scenario.get("user_followups", [])
        if followups:
            random_followup = random.choice(followups)
            phrase = random.choice(topic_change_phrases)
            return f"{phrase}，{random_followup}"
        
        return random.choice(topic_change_phrases)
