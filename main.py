import argparse
import sys
from pathlib import Path
from datetime import datetime
from api_client import XiaomimimoAPIClient
from conversation_splitter import ConversationSplitter
from distiller import ConversationDistiller
from logger import logger
import config


def main():
    parser = argparse.ArgumentParser(description="长对话蒸馏工具 - 从xiaomimimo大模型蒸馏超长对话")
    parser.add_argument("--input", "-i", type=str, help="输入对话文件路径或目录")
    parser.add_argument("--output", "-o", type=str, help="输出文件路径或目录")
    parser.add_argument("--batch", "-b", action="store_true", help="批量处理模式")
    parser.add_argument("--max-tokens", type=int, default=config.MAX_TOKENS, help="每个片段的最大token数")
    parser.add_argument("--overlap-tokens", type=int, default=config.OVERLAP_TOKENS, help="片段间的重叠token数")
    parser.add_argument("--split-method", type=str, default="tokens", choices=["tokens", "turns"], help="分割方法")
    parser.add_argument("--api-key", type=str, default=config.API_KEY, help="API密钥")
    parser.add_argument("--model", type=str, default=config.MODEL, help="使用的模型")

    args = parser.parse_args()

    if not args.input:
        parser.print_help()
        logger.error("请指定输入文件或目录 (--input/-i)")
        sys.exit(1)

    api_client = XiaomimimoAPIClient(api_key=args.api_key, base_url=config.BASE_URL)
    splitter = ConversationSplitter(max_tokens=args.max_tokens, overlap_tokens=args.overlap_tokens)
    distiller = ConversationDistiller(api_client, splitter)

    input_path = Path(args.input)

    def get_unique_output_path(base_path: str, is_dir: bool = False) -> str:
        if is_dir:
            Path(base_path).mkdir(parents=True, exist_ok=True)
            return base_path
        
        path = Path(base_path)
        if path.suffix == '.json':
            base_name = path.stem
            extension = '.json'
        else:
            base_name = path.name
            extension = '.json'
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_name = f"{base_name}_{timestamp}{extension}"
        
        if path.parent != Path('.'):
            output_dir = path.parent
            output_dir.mkdir(parents=True, exist_ok=True)
            return str(output_dir / unique_name)
        
        return unique_name

    if args.batch or input_path.is_dir():
        if not args.output:
            args.output = str(input_path / "output")
        
        output_path = get_unique_output_path(args.output, is_dir=True)
        
        logger.info(f"批量处理模式")
        logger.info(f"输入目录: {input_path}")
        logger.info(f"输出目录: {output_path}")
        
        distiller.batch_distill(str(input_path), output_path)
    else:
        if not input_path.exists():
            logger.error(f"输入文件不存在: {input_path}")
            sys.exit(1)
        
        if not args.output:
            base_name = input_path.stem
            args.output = str(input_path.parent / f"distilled_{base_name}.json")
        
        output_path = get_unique_output_path(args.output, is_dir=False)
        
        logger.info(f"单文件处理模式")
        logger.info(f"输入文件: {input_path}")
        logger.info(f"输出文件: {output_path}")
        
        distiller.distill_conversation_file(str(input_path), output_path)
    
    logger.info("蒸馏完成！")


if __name__ == "__main__":
    main()
