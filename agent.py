from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
print("Ashhad khan 1")

api_key = os.getenv("GEMINI_API_KEY")


provider = AsyncOpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/") 


model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=provider)


scraping_agent = Agent(
    name="ScraperAgent",
    instructions="You are an expert data extraction agent. Extract school events and fees from the provided text.",
    model=model
)

result = Runner.run_sync(scraping_agent, input="")
print(result.final_output)