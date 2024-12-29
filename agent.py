from datetime import datetime
from phi.model.groq import Groq
from phi.agent import Agent
from phi.tools.duckduckgo import DuckDuckGo
from slackBot import get_slack_tools
from dotenv import load_dotenv

load_dotenv()

slack_bot = get_slack_tools()

# Define common constants
MODEL_ID = "llama3-groq-8b-8192-tool-use-preview"
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
SLACK_CHANNEL = "#ai"

# Define news categories and search parameters
NEWS_CATEGORIES = {
    "model_releases": "new AI model releases announcements",
    "multimodal": "multimodal AI developments breakthroughs",
    "agents": "AI agent systems autonomous agents",
    "companies": "OpenAI Anthropic Google DeepMind news updates"
}

# News Bot Definition
news_bot = Agent(
    name="AI News Curator",
    model=Groq(id=MODEL_ID),
    tools=[DuckDuckGo(timeout=120), ],
    description="An intelligent news curator that searches and verifies the latest AI news using DuckDuckGo.",
    instructions=[
        f"You are an AI News Curator responsible for finding and summarizing the latest AI news. "
        "Use DuckDuckGo to search for news from the past 24 hours across key AI categories including "
        "new model releases, multimodal developments, agent systems, and major company updates.",

        "For each relevant result you find:"
        "- Verify it was published within the last 24 hours"
        "- Extract the headline and source URL"
        "- Write a concise 1-2 sentence summary capturing the key points",

        f"Format your findings as a clean news update with the date '{CURRENT_DATE}', "
        "including headlines, summaries and clickable URLs. If no relevant news is found, "
        "simply indicate there are no major updates today.",

        "Keep the update focused and digestible - aim for around 5 of the most significant "
        "and interesting AI news items. Ensure all information is accurate and valuable "
        "for the audience.",

        "The formatted news update will be passed to the Slack bot for distribution "
        f"to the {SLACK_CHANNEL} channel."
    ],
    # debug_mode=True,
    show_tool_calls=True,
    markdown=True
)

# Slack Bot Definition
slack_bot = Agent(
    name="News Distributor",
    tools=[slack_bot],
    model=Groq(id=MODEL_ID),
    description="Your job is to distribute news updates got from the news bot to to slack channel #ai",
    show_tool_calls=True,
    # debug_mode=True,
    markdown=True
)

# Team Coordinator Definition
agent_team = Agent(
    name="AI News Distribution Team",
    team=[news_bot, slack_bot],
    model=Groq(id=MODEL_ID),
    description="Coordinates news gathering and distribution using available tools.",
    instructions=[
        "You are an AI News Distribution Team coordinator. Your role is to gather and distribute the latest AI news.",
        
        "First, coordinate with the news_bot to search and compile AI news using duckduckgo_search. The news_bot will format the results appropriately.",
        
        "Once the news is gathered and properly formatted, work with the slack_bot to distribute the news to the #ai Slack channel using the send_message tool.",
        
        "Ensure seamless coordination between the bots and verify all news is properly formatted before distribution.",
        
        "The process should be fully automated - from news gathering to Slack distribution, requiring minimal human intervention.",
    ],
    show_tool_calls=True,
    debug_mode=True,
    markdown=True
)

def run_news_pipeline():
    """Execute the complete news gathering and distribution pipeline"""
    message = f"""
    EXECUTE THIS SEQUENCE:
    1. Use duckduckgo_search to find AI news from last 24 hours
    2. Send the news to slack channel #ai

    Search categories:
    {NEWS_CATEGORIES.values()}

    Required tools:
    - duckduckgo_search for news gathering
    - send_message for Slack distribution
    """
    
    return agent_team.run(message)

run_news_pipeline()
