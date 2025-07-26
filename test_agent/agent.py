import google.generativeai as genai
from google.adk.agents import Agent

from . import prompt

AGENT_MODEL = "gemini-2.5-pro"

root_agent = Agent(
    model=AGENT_MODEL,
    name="receipt_parser_agent",
    description="parses the receipts",
    instruction=prompt.RECEIPT_PARSER_PROMPT,
    output_key="receipt_parsed_output",
)