# Reddit Questioner

A CLI tool that parses RSS feeds, combines entries, and uses OpenAI to summarize content and answer questions about it.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Set your OpenAI API key as an environment variable:

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