# Reddit Questioner

A CLI tool that parses RSS feeds, combines entries, and uses OpenAI to summarize content and answer questions about it.

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit the `.env` file with your OpenAI API key and preferred settings:

```
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini  # Change to your preferred model
SYSTEM_PROMPT="Your custom system prompt here"
USER_PROMPT_TEMPLATE="Your custom user prompt template here with {content} and {question} placeholders"
```

Alternatively, you can set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY="your-api-key"
```

Run the script:

```bash
python reddit_questioner.py "https://www.reddit.com/r/python/.rss" "What are the trending topics in Python?"
```

## Arguments

- `rss_url`: URL of the RSS feed to parse
- `question`: Question to ask about the RSS feed content

## Output

The tool will output a summary of the RSS feed content followed by an answer to your question.