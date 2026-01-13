import argparse
import sys
import random
import json
import traceback
from pathlib import Path
from api_client import XiaomimimoAPIClient
from conversation_splitter import ConversationSplitter
from distiller import ConversationDistiller
from dual_ai_conversation import DualAIConversation
from logger import logger
import config


def main():
    parser = argparse.ArgumentParser(description="双AI对话生成与蒸馏工具")
    parser.add_argument("--num-conversations", "-n", type=int, default=100, help="生成对话数量")
    parser.add_argument("--min-rounds", type=int, default=50, help="最少对话轮数")
    parser.add_argument("--max-rounds", type=int, default=100, help="最多对话轮数")
    parser.add_argument("--conversation-dir", "-c", type=str, default="./conversations", help="对话保存目录")
    parser.add_argument("--distilled-dir", "-d", type=str, default="./distilled", help="蒸馏结果保存目录")
    parser.add_argument("--max-tokens", type=int, default=config.MAX_TOKENS, help="每个片段的最大token数")
    parser.add_argument("--overlap-tokens", type=int, default=config.OVERLAP_TOKENS, help="片段间的重叠token数")
    parser.add_argument("--api-key", type=str, default=config.API_KEY, help="API密钥")

    args = parser.parse_args()

    api_client = XiaomimimoAPIClient(api_key=args.api_key, base_url=config.BASE_URL)
    splitter = ConversationSplitter(max_tokens=args.max_tokens, overlap_tokens=args.overlap_tokens)
    distiller = ConversationDistiller(api_client, splitter)
    conversation_generator = DualAIConversation(api_client)

    logger.info(f"双AI对话生成与蒸馏工具")
    logger.info(f"生成对话数量: {args.num_conversations}")
    logger.info(f"对话轮数范围: {args.min_rounds} - {args.max_rounds}")
    logger.info(f"对话保存目录: {args.conversation_dir}")
    logger.info(f"蒸馏结果目录: {args.distilled_dir}")

    for i in range(1, args.num_conversations + 1):
        logger.info(f"开始第 {i}/{args.num_conversations} 个对话")

        num_rounds = random.randint(args.min_rounds, args.max_rounds)

        try:
            conversation, scenario = conversation_generator.run_conversation(num_rounds)
            
            conversation_path = conversation_generator.save_conversation(
                conversation, 
                scenario, 
                args.conversation_dir
            )
            
            logger.info(f"开始蒸馏对话...")

            distilled_result = distiller.distill_conversation(conversation)
            
            timestamp = scenario['name']
            distilled_filename = f"distilled_{timestamp}.json"
            distilled_path = Path(args.distilled_dir) / distilled_filename
            
            distilled_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(distilled_path, 'w', encoding='utf-8') as f:
                json.dump(distilled_result, f, ensure_ascii=False, indent=2)
            
            logger.info(f"蒸馏结果已保存到: {distilled_path}")
            logger.info(f"第 {i} 个对话完成！")
            
        except Exception as e:
            logger.error(f"处理第 {i} 个对话时出错: {e}")
            logger.error(traceback.format_exc())
            continue

    logger.info(f"所有对话生成和蒸馏完成！")


if __name__ == "__main__":
    main()
