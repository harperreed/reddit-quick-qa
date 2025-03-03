#!/usr/bin/env python3

import argparse
import feedparser
import openai
import os
import sys
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table

# Load environment variables from .env file
load_dotenv()

class Summary(BaseModel):
    summary: str
    questionAnswer: str
    tone: str
    
# Initialize Rich console
console = Console()


def parse_rss(url: str) -> List[str]:
    """Parse RSS feed entries into a list of strings."""
    feed = feedparser.parse(url)
    
    if not feed.entries:
        print(f"No entries found in feed: {url}", file=sys.stderr)
        sys.exit(1)
    
    entries = []
    for entry in feed.entries:
        title = entry.get('title', '')
        description = entry.get('description', '')
        content = entry.get('content', [{'value': ''}])[0].get('value', '')
        
        # Use content if available, otherwise use description
        text = content if content else description
        entries.append(f"Title: {title}\n\n{text}")
    
    return entries

def mush_content(entries: List[str], max_tokens: int = 16000) -> str:
    """Combine entries into a single text, truncating if necessary."""
    combined = "\n\n---\n\n".join(entries)
    
    # Very rough approximation of tokens (4 chars ~= 1 token)
    chars_per_token = 4
    max_chars = max_tokens * chars_per_token
    
    if len(combined) > max_chars:
        combined = combined[:max_chars] + "... [truncated]"
    
    return combined

def query_openai(content: str, question: str) -> str:
    """Send content and question to OpenAI for summarization and answering."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)
    
    client = openai.OpenAI(api_key=api_key)
    
    # Get model and prompts from environment variables, with defaults
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    system_prompt = os.environ.get(
        "SYSTEM_PROMPT", 
        "You are a helpful assistant that summarizes content and answers questions about it."
    )
    
    # Get the user prompt template and format it with content and question
    user_prompt_template = os.environ.get(
        "USER_PROMPT_TEMPLATE", 
        "Here is content from an RSS feed:\n\n{content}\n\nFirst, provide a brief summary of this content. Then, answer this question about it: {question}"
    )
    user_prompt = user_prompt_template.format(content=content, question=question)
    
    try:
        completion = client.beta.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt_template},
            ],
            response_format=Summary,
        )
        return completion.choices[0].message.parsed
    except Exception as e:
        print(f"Error calling OpenAI API: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Parse Reddit content, summarize it, and answer questions")
    parser.add_argument("subreddit", nargs="?", help="Name of the subreddit (without r/ prefix)")
    parser.add_argument("question", nargs="?", help="Question to ask about the subreddit content")
    args = parser.parse_args()
    
    # If arguments are missing, prompt for them
    if not args.subreddit:
        args.subreddit = console.input("[bold yellow]Enter subreddit name (without r/ prefix): [/]")
    
    if not args.question:
        args.question = console.input("[bold yellow]Enter your question about the subreddit: [/]")
    
    # Construct the RSS URL from the subreddit name
    rss_url = f"https://www.reddit.com/r/{args.subreddit}.rss"
    
    # Show loading message
    with console.status(f"[bold green]Fetching content from r/{args.subreddit}...", spinner="dots"):
        entries = parse_rss(rss_url)
        content = mush_content(entries)
    
    # Display the titles of the feed entries
    console.print("\n[bold cyan]Found these posts:[/]")
    for i, entry in enumerate(entries, 1):
        # Extract title from each entry (assuming format "Title: something\n\nContent...")
        title = entry.split("\n\n")[0].replace("Title: ", "")
        console.print(f"  {i}. [italic]{title}[/]")
    console.print()
    
    with console.status(f"[bold blue]Analyzing r/{args.subreddit} and answering: {args.question}", spinner="point"):
        answer = query_openai(content, args.question)
    
    # Display results with Rich formatting
    console.print(Panel(
        Markdown(f"# r/{args.subreddit} Summary\n\n{answer.summary}"),
        title="Content Summary",
        border_style="green"
    ))
    
    console.print(Panel(
        Markdown(f"## Question\n\n{args.question}\n\n## Answer\n\n{answer.questionAnswer}"),
        title="Q&A",
        border_style="blue"
    ))
    
    # Create a table for metadata
    table = Table(show_header=False, box=None)
    table.add_row("Tone", answer.tone)
    console.print(Panel(table, title="Metadata", border_style="dim"))

if __name__ == "__main__":
    main()
