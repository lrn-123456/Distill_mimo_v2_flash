# 长对话集蒸馏系统

一个基于 xiaomimimo API 的智能对话生成与蒸馏系统，通过模拟真实用户与AI助手之间的多轮对话，生成高质量的长对话数据，并自动进行信息蒸馏提炼。

## 项目简介

本项目旨在解决长对话数据处理的需求，通过双AI对话生成机制，模拟真实用户（包含语法问题和错别字）与AI助手之间的多轮对话，然后对生成的长对话进行智能蒸馏，提炼出核心信息和关键观点。

### 核心价值

- **数据生成**：自动生成多样化、高质量的长对话数据集
- **信息提炼**：通过蒸馏技术从长对话中提取核心知识
- **场景覆盖**：涵盖机器学习、编程、科学知识、日常问题等10种场景
- **真实模拟**：用户模拟器包含约12%的语法问题和错别字，更贴近真实对话

## 功能特点

### 对话生成

- **双AI对话生成**：模拟真实用户（含语法问题和错别字）与AI助手之间的多轮对话
- **多样化场景**：10种不同场景（机器学习入门、Python编程基础、科学知识问答、日常问题解决、技术概念解释、学习方法指导、工具使用技巧、常见错误排查、代码优化建议、项目开发指导）
- **智能话题转移**：当对话停滞时自动转移话题，避免尬聊
- **实时显示**：实时显示AI生成的内容
- **随机轮数**：每轮对话30-100轮随机
- **AI结尾保证**：确保对话以AI回答结尾

### 对话蒸馏

- **自动蒸馏**：对话生成后立即进行蒸馏
- **智能分割**：基于token数或轮数分割长对话
- **片段重叠**：支持片段间重叠，保证信息连续性
- **结构化输出**：蒸馏结果包含对话主题、核心问题、关键观点、重要结论等
- **批量处理**：支持批量处理多个对话文件

## 项目结构

```
distill/
├── api_client.py              # xiaomimimo API客户端封装
├── config.py                 # 全局配置文件
├── conversation_splitter.py   # 对话分割器（基于token或轮数）
├── distiller.py              # 对话蒸馏器
├── dual_ai_conversation.py    # 双AI对话生成器
├── user_simulator.py         # 用户模拟器（含语法问题和错别字）
├── scenarios.py              # 10种场景库
├── main.py                   # 蒸馏工具主程序
├── run.py                    # 对话生成与蒸馏主程序
├── requirements.txt           # Python依赖包
├── example_conversation.json   # 示例对话文件
├── README.md                 # 项目说明文档
├── conversations/            # 对话保存目录
│   └── 机器学习入门_20260112_165404.json
└── distilled/                # 蒸馏结果保存目录
    └── distilled_机器学习入门.json
```

### 核心模块说明

| 模块 | 功能 |
|------|------|
| [api_client.py](api_client.py) | 封装 xiaomimimo API 调用，支持同步和流式响应 |
| [config.py](config.py) | 全局配置，包括API密钥、模型参数、分割参数等 |
| [conversation_splitter.py](conversation_splitter.py) | 对话分割器，支持按token数或轮数分割 |
| [distiller.py](distiller.py) | 对话蒸馏器，提炼核心信息并生成摘要 |
| [dual_ai_conversation.py](dual_ai_conversation.py) | 双AI对话生成器，模拟用户与AI助手对话 |
| [user_simulator.py](user_simulator.py) | 用户模拟器，添加语法问题和错别字 |
| [scenarios.py](scenarios.py) | 场景库，定义10种对话场景 |

## 部署指南

### 环境要求

- Python 3.8+
- 稳定的网络连接（访问 xiaomimimo API）
- xiaomimimo API 密钥

### 安装步骤

1. **克隆或下载项目**

```bash
cd distill
```

2. **安装依赖**

```bash
pip install -r requirements.txt
```

依赖包包括：
- `requests>=2.31.0` - HTTP请求库
- `tiktoken>=0.5.0` - Token计数工具

3. **配置API密钥**

编辑 [config.py](config.py) 文件，设置你的API密钥：

```python
API_KEY = "your_api_key_here"  # 替换为你的 xiaomimimo API 密钥
BASE_URL = "https://api.xiaomimimo.com/v1"
MODEL = "mimo-v2-flash"
```

4. **验证配置**

运行以下命令验证配置是否正确：

```bash
python -c "from api_client import XiaomimimoAPIClient; import config; client = XiaomimimoAPIClient(config.API_KEY); print('配置成功！')"
```

## 使用方法

### 方式一：生成对话并自动蒸馏

使用 [run.py](run.py) 生成对话并自动进行蒸馏。

#### 基本用法

```bash
# 生成3个对话，每个30-100轮
python run.py -n 3
```

#### 高级用法

```bash
# 生成5个对话，指定轮数范围
python run.py -n 5 --min-rounds 50 --max-rounds 100

# 自定义保存目录
python run.py -n 2 -c ./my_conversations -d ./my_distilled

# 自定义token分割参数
python run.py -n 3 --max-tokens 3000 --overlap-tokens 100

# 使用自定义API密钥
python run.py -n 3 --api-key your_custom_api_key
```

#### 参数说明

| 参数 | 简写 | 默认值 | 说明 |
|------|--------|---------|------|
| --num-conversations | -n | 100 | 生成对话数量 |
| --min-rounds | | 50 | 最少对话轮数 |
| --max-rounds | | 100 | 最多对话轮数 |
| --conversation-dir | -c | ./conversations | 对话保存目录 |
| --distilled-dir | -d | ./distilled | 蒸馏结果保存目录 |
| --max-tokens | | 4000 | 每个片段的最大token数 |
| --overlap-tokens | | 200 | 片段间的重叠token数 |
| --api-key | | | API密钥（默认使用config.py中的配置） |

### 方式二：仅蒸馏现有对话

使用 [main.py](main.py) 对已有的对话文件进行蒸馏。

#### 单文件蒸馏

```bash
# 蒸馏单个对话文件
python main.py -i example_conversation.json

# 指定输出文件
python main.py -i example_conversation.json -o output.json

# 自定义分割参数
python main.py -i example_conversation.json --max-tokens 3000 --overlap-tokens 100
```

#### 批量蒸馏

```bash
# 批量处理目录下的所有对话文件
python main.py -i ./conversations -b

# 指定输出目录
python main.py -i ./conversations -b -o ./output

# 按轮数分割
python main.py -i ./conversations -b --split-method turns
```

#### 参数说明

| 参数 | 简写 | 默认值 | 说明 |
|------|--------|---------|------|
| --input | -i | | 输入对话文件路径或目录 |
| --output | -o | | 输出文件路径或目录 |
| --batch | -b | False | 批量处理模式 |
| --max-tokens | | 4000 | 每个片段的最大token数 |
| --overlap-tokens | | 200 | 片段间的重叠token数 |
| --split-method | | tokens | 分割方法（tokens/turns） |
| --api-key | | | API密钥 |
| --model | | | 使用的模型 |

## 输出格式

### 对话文件格式

对话文件保存在 `conversations/` 目录下，格式如下：

```json
{
  "scenario": {
    "name": "机器学习入门",
    "description": "用户询问机器学习基础概念，AI进行讲解和答疑",
    "user_prompt": "我想学习机器学习，但是不知道从哪里开始，能给我一些建议吗？",
    "ai_role": "你是一个机器学习专家，擅长用通俗易懂的方式讲解复杂概念。请从实际应用角度帮助用户理解。",
    "user_followups": [
      "监督学习和无监督学习有啥区别",
      "什么是过拟合和欠拟合",
      "怎么选择合适的算法"
    ]
  },
  "conversation": [
    {
      "role": "user",
      "content": "我想学习机器学习，但是不知道从哪里开始，能给我一些建议吗？"
    },
    {
      "role": "assistant",
      "content": "学习机器学习是一个很好的选择！我建议你从以下几个方面开始..."
    }
  ],
  "total_rounds": 50,
  "created_at": "2026-01-11T19:43:32"
}
```

### 蒸馏结果格式

蒸馏结果保存在 `distilled/` 目录下，格式如下：

```json
{
  "total_chunks": 4,
  "distilled_chunks": [
    {
      "chunk_index": 0,
      "original_messages": [
        {
          "role": "user",
          "content": "..."
        },
        {
          "role": "assistant",
          "content": "..."
        }
      ],
      "distilled_content": "对话主题：机器学习入门\n\n核心问题：\n- 如何开始学习机器学习\n- 监督学习和无监督学习的区别\n\n关键观点：\n- 机器学习是人工智能的一个分支\n- 需要掌握数学基础\n- 实践项目很重要\n\n重要结论：\n- 建议从基础概念开始学习\n- 结合实践项目加深理解"
    }
  ],
  "final_summary": "整体对话主题：机器学习入门指导\n\n主要讨论的问题：\n1. 机器学习的基础概念和分类\n2. 学习机器学习需要的数学基础\n3. 推荐的学习资源和实践项目\n4. 常见的算法选择和模型评估\n\n核心观点和结论：\n- 机器学习需要扎实的数学基础\n- 理论学习与实践相结合\n- 从简单项目开始逐步深入\n- 持续学习和实践是关键"
}
```

## 场景列表

系统内置10种对话场景，覆盖多个领域：

| 序号 | 场景名称 | 描述 |
|------|----------|------|
| 1 | 机器学习入门 | 用户询问机器学习基础概念，AI进行讲解和答疑 |
| 2 | Python编程基础 | 用户学习Python编程，AI提供指导和答疑 |
| 3 | 科学知识问答 | 用户询问科学知识，AI进行科普讲解 |
| 4 | 日常问题解决 | 用户遇到日常问题，AI提供解决方案 |
| 5 | 技术概念解释 | 用户询问技术概念，AI进行讲解 |
| 6 | 学习方法指导 | 用户询问学习方法，AI提供指导建议 |
| 7 | 工具使用技巧 | 用户询问工具使用，AI提供技巧指导 |
| 8 | 常见错误排查 | 用户遇到错误问题，AI帮助排查 |
| 9 | 代码优化建议 | 用户询问代码优化，AI提供建议 |
| 10 | 项目开发指导 | 用户开发项目，AI提供指导 |

## 技术架构

### 系统流程

```
┌─────────────────┐
│  场景选择       │
│  (scenarios.py) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  双AI对话生成   │
│  (dual_ai_      │
│   conversation) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  用户模拟       │
│  (user_         │
│   simulator)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  对话保存       │
│  (JSON格式)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  对话分割       │
│  (conversation  │
│   _splitter)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  对话蒸馏       │
│  (distiller)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  结果保存       │
│  (JSON格式)     │
└─────────────────┘
```

### 关键技术

1. **API调用**：基于 requests 库封装 xiaomimimo API
2. **流式响应**：支持流式输出，实时显示AI生成内容
3. **Token计数**：使用 tiktoken 精确计算token数
4. **对话分割**：支持按token数或轮数分割长对话
5. **用户模拟**：添加语法问题、错别字、口语化表达等
6. **话题转移**：智能检测对话停滞，自动转移话题

## 配置说明

### config.py 配置项

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| API_KEY | | xiaomimimo API密钥（必填） |
| BASE_URL | https://api.xiaomimimo.com/v1 | API基础URL |
| MODEL | mimo-v2-flash | 使用的模型 |
| MAX_TOKENS | 4000 | 每个片段的最大token数 |
| OVERLAP_TOKENS | 200 | 片段间的重叠token数 |
| MAX_TURNS | 10 | 按轮数分割时的最大轮数 |
| TEMPERATURE | 0.3 | 蒸馏时的温度参数 |
| MAX_OUTPUT_TOKENS | 2000 | 最大输出token数 |
| REQUEST_TIMEOUT | 120 | 请求超时时间（秒） |
| RETRY_DELAY | 1 | 重试延迟（秒） |
| MAX_RETRIES | 3 | 最大重试次数 |

## 注意事项

1. **API密钥配置**：确保 [config.py](config.py) 中的 API_KEY 配置正确
2. **网络连接**：确保能够访问 xiaomimimo API 服务
3. **对话结尾**：对话以AI回答结尾，如果最后一条是用户消息会自动移除
4. **文件命名**：
   - 对话文件以"场景名称_时间戳.json"格式命名
   - 蒸馏结果以"distilled_场景名称.json"格式命名
5. **用户模拟**：用户模拟器会随机出现约12%的语法问题和错别字
6. **话题转移**：当检测到对话停滞时，会自动转移话题
7. **资源消耗**：生成大量对话会消耗API配额，请根据需求调整参数

## 常见问题

### Q: 如何获取 xiaomimimo API 密钥？

A: 访问 xiaomimimo 官网注册账号，在控制台创建API密钥。

### Q: 生成对话很慢怎么办？

A: 可以减少 `--num-conversations` 参数，或者调整 `--min-rounds` 和 `--max-rounds` 范围。

### Q: 蒸馏结果不准确怎么办？

A: 可以调整 `--max-tokens` 参数，使每个片段包含更多上下文信息。

### Q: 如何自定义场景？

A: 编辑 [scenarios.py](scenarios.py) 文件，在 `SCENARIOS` 列表中添加新场景。

### Q: 如何处理API请求失败？

A: 检查网络连接和API密钥配置，系统会自动重试最多3次。

## 许可证

本项目仅供学习和研究使用。

## 联系方式

如有问题或建议，欢迎提出 Issue。
