# Long Conversation Distillation System

An intelligent conversation generation and distillation system based on xiaomimimo API. It generates high-quality long conversation data by simulating multi-turn conversations between real users (with grammar issues and typos) and AI assistants, and automatically performs information distillation to extract core insights.

## Project Overview

This project addresses the need for processing long conversation data. Through a dual-AI conversation generation mechanism, it simulates multi-turn conversations between real users (including grammar issues and typos) and AI assistants, then intelligently distills the generated long conversations to extract core information and key insights.

### Core Value

- **Data Generation**: Automatically generate diverse, high-quality long conversation datasets
- **Information Extraction**: Extract core knowledge from long conversations through distillation technology
- **Scenario Coverage**: Covers 10 scenarios including machine learning, programming, scientific knowledge, and daily problems
- **Realistic Simulation**: User simulator includes approximately 12% grammar issues and typos for more realistic conversations

## Features

### Conversation Generation

- **Dual-AI Conversation Generation**: Simulates multi-turn conversations between real users (with grammar issues and typos) and AI assistants
- **Diverse Scenarios**: 10 different scenarios (Machine Learning Basics, Python Programming, Science Q&A, Daily Problem Solving, Technical Concepts, Learning Methods, Tool Usage, Error Debugging, Code Optimization, Project Development)
- **Smart Topic Transition**: Automatically transitions topics when conversation stalls to avoid awkward pauses
- **Real-time Display**: Displays AI-generated content in real-time
- **Random Rounds**: 30-100 rounds per conversation randomly
- **AI Ending Guarantee**: Ensures conversations end with AI responses

### Conversation Distillation

- **Automatic Distillation**: Immediately distills conversations after generation
- **Smart Splitting**: Splits long conversations based on token count or number of turns
- **Chunk Overlap**: Supports overlap between chunks to ensure information continuity
- **Structured Output**: Distillation results include conversation topics, core questions, key insights, important conclusions, etc.
- **Batch Processing**: Supports batch processing of multiple conversation files

## Project Structure

```
distill/
├── api_client.py              # xiaomimimo API client wrapper
├── config.py                 # Global configuration file
├── conversation_splitter.py   # Conversation splitter (based on tokens or turns)
├── distiller.py              # Conversation distiller
├── dual_ai_conversation.py    # Dual-AI conversation generator
├── user_simulator.py         # User simulator (with grammar issues and typos)
├── scenarios.py              # 10 scenario library
├── main.py                   # Distillation tool main program
├── run.py                    # Conversation generation and distillation main program
├── requirements.txt           # Python dependencies
├── example_conversation.json   # Example conversation file
├── README.md                 # Project documentation (Chinese)
├── README_EN.md              # Project documentation (English)
├── logger.py                 # Logging module
├── .gitignore               # Git ignore file
├── conversations/            # Conversation save directory
│   └── MachineLearning_20260112_165404.json
└── distilled/                # Distillation result save directory
    └── distilled_MachineLearning.json
```

### Core Module Description

| Module | Function |
|--------|----------|
| [api_client.py](api_client.py) | Wraps xiaomimimo API calls, supports synchronous and streaming responses |
| [config.py](config.py) | Global configuration, including API key, model parameters, splitting parameters, etc. |
| [conversation_splitter.py](conversation_splitter.py) | Conversation splitter, supports splitting by token count or number of turns |
| [distiller.py](distiller.py) | Conversation distiller, extracts core information and generates summaries |
| [dual_ai_conversation.py](dual_ai_conversation.py) | Dual-AI conversation generator, simulates user-AI conversations |
| [user_simulator.py](user_simulator.py) | User simulator, adds grammar issues and typos |
| [scenarios.py](scenarios.py) | Scenario library, defines 10 conversation scenarios |

## Deployment Guide

### Environment Requirements

- Python 3.8+
- Stable network connection (access to xiaomimimo API)
- xiaomimimo API key

### Installation Steps

1. **Clone or Download Project**

```bash
cd distill
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

Dependencies include:
- `requests>=2.31.0` - HTTP request library
- `tiktoken>=0.5.0` - Token counting tool

3. **Configure API Key**

Edit [config.py](config.py) file and set your API key:

```python
API_KEY = "your_api_key_here"  # Replace with your xiaomimimo API key
BASE_URL = "https://api.xiaomimimo.com/v1"
MODEL = "mimo-v2-flash"
```

4. **Verify Configuration**

Run the following command to verify configuration:

```bash
python -c "from api_client import XiaomimimoAPIClient; import config; client = XiaomimimoAPIClient(config.API_KEY); print('Configuration successful!')"
```

## Usage

### Method 1: Generate Conversations and Auto-Distill

Use [run.py](run.py) to generate conversations and automatically distill them.

#### Basic Usage

```bash
# Generate 3 conversations, each with 30-100 rounds
python run.py -n 3
```

#### Advanced Usage

```bash
# Generate 5 conversations, specify round range
python run.py -n 5 --min-rounds 50 --max-rounds 100

# Custom save directories
python run.py -n 2 -c ./my_conversations -d ./my_distilled

# Custom token splitting parameters
python run.py -n 3 --max-tokens 3000 --overlap-tokens 100

# Use custom API key
python run.py -n 3 --api-key your_custom_api_key
```

#### Parameter Description

| Parameter | Short | Default | Description |
|-----------|--------|----------|-------------|
| --num-conversations | -n | 100 | Number of conversations to generate |
| --min-rounds | | 50 | Minimum number of conversation rounds |
| --max-rounds | | 100 | Maximum number of conversation rounds |
| --conversation-dir | -c | ./conversations | Conversation save directory |
| --distilled-dir | -d | ./distilled | Distillation result save directory |
| --max-tokens | | 4000 | Maximum tokens per chunk |
| --overlap-tokens | | 200 | Overlap tokens between chunks |
| --api-key | | | API key (uses config.py configuration by default) |

### Method 2: Distill Existing Conversations Only

Use [main.py](main.py) to distill existing conversation files.

#### Single File Distillation

```bash
# Distill a single conversation file
python main.py -i example_conversation.json

# Specify output file
python main.py -i example_conversation.json -o output.json

# Custom splitting parameters
python main.py -i example_conversation.json --max-tokens 3000 --overlap-tokens 100
```

#### Batch Distillation

```bash
# Batch process all conversation files in directory
python main.py -i ./conversations -b

# Specify output directory
python main.py -i ./conversations -b -o ./output

# Split by turns
python main.py -i ./conversations -b --split-method turns
```

#### Parameter Description

| Parameter | Short | Default | Description |
|-----------|--------|----------|-------------|
| --input | -i | | Input conversation file path or directory |
| --output | -o | | Output file path or directory |
| --batch | -b | False | Batch processing mode |
| --max-tokens | | 4000 | Maximum tokens per chunk |
| --overlap-tokens | | 200 | Overlap tokens between chunks |
| --split-method | | tokens | Splitting method (tokens/turns) |
| --api-key | | | API key |
| --model | | | Model to use |

## Output Format

### Conversation File Format

Conversation files are saved in the `conversations/` directory with the following format:

```json
{
  "scenario": {
    "name": "Machine Learning Basics",
    "description": "User asks about machine learning basics, AI explains and answers questions",
    "user_prompt": "I want to learn machine learning but don't know where to start. Can you give me some suggestions?",
    "ai_role": "You are a machine learning expert, good at explaining complex concepts in simple terms. Help users understand from a practical application perspective.",
    "user_followups": [
      "What's the difference between supervised and unsupervised learning",
      "What are overfitting and underfitting",
      "How to choose the right algorithm"
    ]
  },
  "conversation": [
    {
      "role": "user",
      "content": "I want to learn machine learning but don't know where to start. Can you give me some suggestions?"
    },
    {
      "role": "assistant",
      "content": "Learning machine learning is a great choice! I suggest you start from the following aspects..."
    }
  ],
  "total_rounds": 50,
  "created_at": "2026-01-11T19:43:32"
}
```

### Distillation Result Format

Distillation results are saved in the `distilled/` directory with the following format:

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
      "distilled_content": "Conversation Topic: Machine Learning Basics\n\nCore Questions:\n- How to start learning machine learning\n- Difference between supervised and unsupervised learning\n\nKey Insights:\n- Machine learning is a branch of AI\n- Need to master mathematical foundations\n- Practical projects are important\n\nImportant Conclusions:\n- Suggest starting from basic concepts\n- Combine with practical projects to deepen understanding"
    }
  ],
  "final_summary": "Overall Conversation Topic: Machine Learning Basics Guidance\n\nMain Issues Discussed:\n1. Basic concepts and classification of machine learning\n2. Mathematical foundations needed for learning machine learning\n3. Recommended learning resources and practical projects\n4. Common algorithm selection and model evaluation\n\nCore Insights and Conclusions:\n- Machine learning requires solid mathematical foundations\n- Combine theoretical learning with practice\n- Start with simple projects and gradually deepen\n- Continuous learning and practice are key"
}
```

## Scenario List

The system includes 10 built-in conversation scenarios covering multiple domains:

| No. | Scenario Name | Description |
|------|--------------|-------------|
| 1 | Machine Learning Basics | User asks about machine learning basics, AI explains and answers questions |
| 2 | Python Programming Basics | User learns Python programming, AI provides guidance and answers |
| 3 | Science Q&A | User asks about scientific knowledge, AI provides popular science explanations |
| 4 | Daily Problem Solving | User encounters daily problems, AI provides solutions |
| 5 | Technical Concepts | User asks about technical concepts, AI provides explanations |
| 6 | Learning Methods | User asks about learning methods, AI provides guidance |
| 7 | Tool Usage Tips | User asks about tool usage, AI provides tips |
| 8 | Error Debugging | User encounters error issues, AI helps debug |
| 9 | Code Optimization | User asks about code optimization, AI provides suggestions |
| 10 | Project Development | User develops projects, AI provides guidance |

## Technical Architecture

### System Flow

```
┌─────────────────┐
│  Scenario Select │
│  (scenarios.py) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Dual-AI Conv  │
│  (dual_ai_      │
│   conversation) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  User Simulate │
│  (user_         │
│   simulator)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Conv Save     │
│  (JSON format) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Conv Split    │
│  (conversation  │
│   _splitter)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Conv Distill  │
│  (distiller)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Result Save   │
│  (JSON format) │
└─────────────────┘
```

### Key Technologies

1. **API Calls**: Wraps xiaomimimo API based on requests library
2. **Streaming Response**: Supports streaming output, displays AI-generated content in real-time
3. **Token Counting**: Uses tiktoken for accurate token counting
4. **Conversation Splitting**: Supports splitting long conversations by token count or number of turns
5. **User Simulation**: Adds grammar issues, typos, colloquial expressions, etc.
6. **Topic Transition**: Intelligently detects conversation stagnation and automatically transitions topics

## Configuration

### config.py Configuration Items

| Configuration | Default | Description |
|---------------|----------|-------------|
| API_KEY | | xiaomimimo API key (required) |
| BASE_URL | https://api.xiaomimimo.com/v1 | API base URL |
| MODEL | mimo-v2-flash | Model to use |
| MAX_TOKENS | 4000 | Maximum tokens per chunk |
| OVERLAP_TOKENS | 200 | Overlap tokens between chunks |
| MAX_TURNS | 10 | Maximum turns when splitting by turns |
| TEMPERATURE | 0.3 | Temperature parameter for distillation |
| MAX_OUTPUT_TOKENS | 2000 | Maximum output tokens |
| REQUEST_TIMEOUT | 120 | Request timeout (seconds) |
| RETRY_DELAY | 1 | Retry delay (seconds) |
| MAX_RETRIES | 3 | Maximum retry attempts |

## Notes

1. **API Key Configuration**: Ensure API_KEY in [config.py](config.py) is configured correctly
2. **Network Connection**: Ensure access to xiaomimimo API service
3. **Conversation Ending**: Conversations end with AI responses; if the last message is from a user, it will be automatically removed
4. **File Naming**:
   - Conversation files are named in "ScenarioName_Timestamp.json" format
   - Distillation results are named in "distilled_ScenarioName.json" format
5. **User Simulation**: User simulator randomly includes approximately 12% grammar issues and typos
6. **Topic Transition**: Automatically transitions topics when conversation stagnation is detected
7. **Resource Consumption**: Generating many conversations consumes API quota; adjust parameters according to needs

## FAQ

### Q: How to get xiaomimimo API key?

A: Visit the xiaomimimo official website to register an account and create an API key in the console.

### Q: What if conversation generation is slow?

A: You can reduce the `--num-conversations` parameter, or adjust the `--min-rounds` and `--max-rounds` ranges.

### Q: What if distillation results are inaccurate?

A: You can adjust the `--max-tokens` parameter to include more context information in each chunk.

### Q: How to customize scenarios?

A: Edit [scenarios.py](scenarios.py) file and add new scenarios to the `SCENARIOS` list.

### Q: How to handle API request failures?

A: Check network connection and API key configuration; the system will automatically retry up to 3 times.

## License

This project is for learning and research purposes only.

## Contact

For questions or suggestions, feel free to submit an Issue.
