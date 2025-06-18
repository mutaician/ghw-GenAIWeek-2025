# 🐦 AI Tweet Generation Agent

This Streamlit application uses AI agents, powered by Clarifai and CrewAI, to generate high-quality, engaging tweets from your daily learnings or any other text you provide.

## ✨ Features

- **AI-Powered Content Creation**: Leverages AI agents to summarize your text and craft compelling tweets.
- **Real-Time Web Search**: The tweeter agent can search the web to find relevant Twitter handles for mentions.
- **Character-Limited Output**: Ensures the generated tweet is under 280 characters, ready for posting.
- **Hashtag Generation**: Automatically includes relevant hashtags to increase engagement.
- **Copy to Clipboard**: Easily copy the generated tweet with a single click.

## 🛠️ Setup

### 1. Clone the Repository

```bash
git clone https://github.com/mutaician/ghw-GenAIWeek-2025.git
cd genAiWk2025/clarifai-agent
```

### 2. Install Dependencies

This project uses `uv` for package management. You can install the dependencies using the following command:

```bash
pip install uv
uv pip install -r requirements.txt
```

### 3. Set Environment Variables

Create a `.env` file in the root of the project and add the following environment variables:

```
CLARIFAI_PAT="your_clarifai_personal_access_token"
SERPER_API_KEY="your_serper_dev_api_key"
```

- `CLARIFAI_PAT`: Your Personal Access Token from Clarifai.
- `SERPER_API_KEY`: Your API key from Serper.dev for search functionalities.

## 🚀 Running the Application

To run the Streamlit application, use the following command:

```bash
streamlit run main.py
```

This will open the application in your web browser.

## Usage

1.  Enter the text you want to tweet about in the text area.
2.  Click the "🚀 Generate Tweet" button.
3.  The AI agents will process your text and generate a tweet.
4.  You can then copy the tweet to your clipboard using the "📥 Copy Tweet" button.
