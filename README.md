# 📖 Reddit Questioner

Welcome to the **Reddit Questioner**! This is a CLI tool that helps you explore Reddit content by parsing RSS feeds, summarizing entries, and answering specific questions about the content using OpenAI's language model. 🚀

## 🔍 Summary of Project

The **Reddit Questioner** allows users to input a subreddit and a question related to that subreddit. The tool fetches the latest posts, summarizes the content, and provides answers based on the user’s query. This application utilizes OpenAI's API to generate responses and is ideal for users wanting quick insights into trending topics or specific discussions on Reddit.

## 🛠️ How to Use

To get started with the **Reddit Questioner**, follow these simple steps:

### 1. Configuration

You need to set up your environment variables by creating a `.env` file. Use the provided example as a template:

```bash
cp .env.example .env
```

Edit the `.env` file with your OpenAI API key and any other settings you'd like to modify:

```bash
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini  # Change to your preferred model
SYSTEM_PROMPT="Your custom system prompt here"
USER_PROMPT_TEMPLATE="Your custom user prompt template here with {content} and {question} placeholders"
```

Alternatively, you can export the OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY="your-api-key"
```

### 2. Running the Tool

To run the **Reddit Questioner**, use the following command, replacing the placeholders with your desired subreddit and question:

```bash
uv reddit_questioner.py python "What are the trending topics in Python?"
```

### 3. Arguments

- `subreddit`: Name of the subreddit (without r/ prefix)
- `question`: The question you wish to ask regarding the RSS feed content

### 4. Output

The tool will parse the RSS feed, summarize the content, and provide an answer to your question. The output will include the summary and Q&A in a nicely formatted display. 🎉

## 🛠️ Tech Info

This project is built with the following technologies:

- **Python**: Programming language for the CLI application.
- **OpenAI API**: Utilized for summarization and question answering.
- **Rich**: A Python library for building beautiful rich text outputs.
- **Feedparser**: A library to handle the RSS feed parsing.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **dotenv**: For loading environment variables from a `.env` file.
- **Fake User-Agent**: Generates random user-agent strings for HTTP requests.

### Project Structure 🗂️

- `.env.example`: Example environment variables file.
- `.gitignore`: Files and directories ignored by Git.
- `.python-version`: Python version specification.
- `pyproject.toml`: Project dependencies and metadata.
- `reddit_questioner.py`: Main application script.
- `README.md`: This file.

Feel free to explore and contribute to make the **Reddit Questioner** even better! If you encounter any issues or have feature requests, please open an issue in this repository. Happy questioning! 🤖

---

For any inquiries, reach out to me on GitHub: [Harper Reed](https://github.com/harperreed) 💻
