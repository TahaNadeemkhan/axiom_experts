from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel
from agents.run_config import RunConfig
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

print("ABDULLAH ZUNORAIN")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not set. Add it to .env or your environment.")

provider = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

requested_model = os.getenv("GEMINI_MODEL")
model_name = requested_model or "gemini-1.5-flash"

async def _pick_model(client: AsyncOpenAI, requested: str | None) -> str:
    try:
        models = await client.models.list()
        available = [m.id for m in models.data]
        if requested and requested in available:
            return requested
        preferred_order = [
            "gemini-2.0-flash",
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-1.5-flash-8b",
        ]
        return next((m for m in preferred_order if m in available), available[0])
    except Exception:
        return requested or "gemini-1.5-flash"

model_name = asyncio.run(_pick_model(provider, requested_model))

model = OpenAIChatCompletionsModel(model=model_name, openai_client=provider)


scraping_agent = Agent(
    name="ScraperAgent",
    instructions="You are a Cyber Security Expert.",
    model=model
)

result = Runner.run_sync(
    scraping_agent,
    input="Give a short cybersecurity tip.",
    run_config=RunConfig(tracing_disabled=True),
)
print(result.final_output)
