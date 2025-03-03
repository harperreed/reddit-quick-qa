#!/usr/bin/env python3

import argparse
import feedparser
import openai
import os
import sys
from typing import List

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
    
    system_prompt = "You are a helpful assistant that summarizes content and answers questions about it."
    user_prompt = f"Here is content from an RSS feed:\n\n{content}\n\nFirst, provide a brief summary of this content. Then, answer this question about it: {question}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Parse RSS feed, summarize content, and answer questions")
    parser.add_argument("rss_url", help="URL of the RSS feed to parse")
    parser.add_argument("question", help="Question to ask about the RSS feed content")
    args = parser.parse_args()
    
    entries = parse_rss(args.rss_url)
    content = mush_content(entries)
    answer = query_openai(content, args.question)
    
    print(answer)

if __name__ == "__main__":
    main()