import streamlit as st
import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
from st_copy_to_clipboard import st_copy_to_clipboard


# Environment variables
CLARIFAI_PAT = os.getenv("CLARIFAI_PAT")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

if not CLARIFAI_PAT:
    st.error("Please set CLARIFAI_PAT environment variable")
    st.stop()

if not SERPER_API_KEY:
    st.error("Please set SERPER_API_KEY environment variable")
    st.stop()

# Configure Clarifai LLM
clarifai_llm = LLM(
    model="openai/gcp/generate/models/gemini-2_5-flash",
    api_key=CLARIFAI_PAT,
    base_url="https://api.clarifai.com/v2/ext/openai/v1"
)

# Initialize tools
search_tool = SerperDevTool()

# Define Agents
summarizer = Agent(
    role="Expert Content Summarizer",
    goal="Summarize the key takeaways from the provided text to make them tweetable.",
    backstory="""You are an expert in distilling information into concise, impactful summaries. 
    You can identify the most important points and prepare them for social media.""",
    verbose=True,
    allow_delegation=False,
    llm=clarifai_llm,
    max_iter=3,
)

tweeter = Agent(
    role="Professional Twitter Content Creator",
    goal="Create a viral-worthy tweet from a given summary, including relevant hashtags and mentions.",
    backstory="""You are a social media wizard, an expert in crafting tweets that get maximum engagement. 
    You know how to use hashtags, mentions, and concise language to make a point and go viral.""",
    tools=[search_tool],
    verbose=True,
    allow_delegation=True,
    llm=clarifai_llm,
    max_iter=3,
)

def create_tasks(learnings):
    """Create summarization and tweet generation tasks for the given learnings"""
    summarization_task = Task(
        description=f"""Analyze the following text of learnings and extract 1-3 key, impactful points 
        that are suitable for a social media post. Focus on what would be most interesting to a general tech audience.
        
        Learnings:
        '{learnings}'""",
        expected_output="A concise list of bullet points summarizing the core ideas.",
        agent=summarizer
    )

    tweet_creation_task = Task(
        description=f"""Based on the provided key points, write a tweet. 
        The tweet must be engaging, informative, and **under 280 characters**. 
        Include 2-4 relevant hashtags. If a specific technology or person is mentioned, 
        use the search tool to find their Twitter handle to tag them.
        
        IMPORTANT: The final output should be ONLY the tweet text. No extra titles, just the tweet.""",
        expected_output="A single, perfectly formatted tweet, ready to be posted.",
        agent=tweeter,
        context=[summarization_task]
    )
    
    return summarization_task, tweet_creation_task

def run_tweet_generation(learnings):
    """Run the tweet generation crew for the given learnings"""
    summarization_task, tweet_creation_task = create_tasks(learnings)
    
    crew = Crew(
        agents=[summarizer, tweeter],
        tasks=[summarization_task, tweet_creation_task],
        process=Process.sequential,
        verbose=True
    )
    result = crew.kickoff()
    
    return result

# Streamlit App
def main():
    st.title("🐦 AI Tweet Generation Agent")
    st.markdown("*Powered by Clarifai & CrewAI*")

    st.markdown("""
    This application uses AI agents to generate a high-quality tweet based on your daily learnings.
    
    **How it works:**
    - 📝 **Summarizer Agent** extracts the key points from your text.
    - 🐦 **Tweeter Agent** crafts an engaging, short-form tweet with hashtags.
    - 🧠 **Powered by** Clarifai's models via OpenAI-compatible API.
    """)

    # Input section
    with st.container():
        learnings = st.text_area(
            "What did you learn today?",
            placeholder="e.g., I learned about how CrewAI can be used to create autonomous agents for different tasks...",
            height=150,
            help="Provide a summary of your learnings for the AI to process."
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            generate_button = st.button("🚀 Generate Tweet", type="primary")

    # Generation section
    if generate_button:
        if not learnings.strip():
            st.error("Please enter what you learned today.")
        else:
            with st.spinner(f"🧠 AI agents are crafting a tweet about your learnings..."):
                try:
                    result = run_tweet_generation(learnings)
                    
                    st.success("✅ Tweet generated successfully!")
                    st.markdown("---")
                    
                    # Display the result
                    st.markdown(str(result))
                    
                    # Copy to clipboard option
                    st_copy_to_clipboard(str(result), "📥 Copy Tweet")
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

    # Sidebar
    with st.sidebar:
        st.header("ℹ️ Information")
        
        st.markdown("**Environment Variables Required:**")
        st.code("CLARIFAI_PAT=your_clarifai_personal_access_token")
        st.code("SERPER_API_KEY=your_serper_dev_api_key")
        
        st.markdown("**Current Configuration:**")
        st.markdown(f"- **Model:** `gcp/generate/models/gemini-2_5-pro` (or similar)")
        st.markdown(f"- **API Base:** `api.clarifai.com`")
        
        st.markdown("**Features:**")
        st.markdown("- Real-time web search for hashtags/mentions")
        st.markdown("- AI-powered content summarization & creation")
        st.markdown("- Character-limited output for Twitter")
        st.markdown("- Copy to clipboard capability")
        

if __name__ == "__main__":
    main()