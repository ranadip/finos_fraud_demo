from google.adk.sessions import VertexAiSessionService
from google import adk
from agent import root_agent as agent
from google.genai import types
import asyncio

LOCATION="us-central1"
PROJECT_ID="lighthouse-342811"
# MODEL_NAME="gemini-2.0-flash-001"
# EMBEDDING_MODEL_NAME="gemini-embedding-001"
AGENT_ENGINE_NAME="projects/lighthouse-342811/locations/us-central1/reasoningEngines/4930711516249849856" #FSI Fraud Agent Demo
USER_ID="testuser"

import logging
logging.basicConfig(level=logging.INFO)
logging.debug("test")

session_service = VertexAiSessionService(
  PROJECT_ID, LOCATION)

runner = adk.Runner(
    agent=agent,
    app_name=AGENT_ENGINE_NAME,
    session_service=session_service
    )
print(f"Runner created for agent '{runner.agent.name}'.")

async def call_agent(query, session, user_id):
  content = types.Content(role='user', parts=[types.Part(text=query)])
  events = runner.run_async(user_id=user_id, session_id=session, new_message=content)

  async for event in events:
      if event.is_final_response():
          final_response = event.content.parts[0].text
          print("Agent Response: ", final_response)

  print(f"<<< Agent Response: {final_response}")
  return final_response



async def run_conversation():
    session = await session_service.create_session(
    app_name=AGENT_ENGINE_NAME,
    user_id=USER_ID
    )

    await call_agent(
    "Can you update the temperature to my preferred temperature?",
    session.id,
    USER_ID)

    # Agent response: "What is your preferred temperature?"
    await call_agent("I like it at 71 degrees", session.id, USER_ID)
    # Agent Response:  Setting the temperature to 71 degrees Fahrenheit.
    # Temperature successfully changed.

async def run_conversation_w_prompt(prompt):
    session = await session_service.create_session(
    app_name=AGENT_ENGINE_NAME,
    user_id=USER_ID
    )

    response = await call_agent(
    prompt,
    session.id,
    USER_ID)

    return response

import traceback
from fastapi import FastAPI, Request
if __name__ == "__main__":
    try:
        asyncio.run(run_conversation())
    except Exception as e:
        print(f"An error occurred: {e}")
        print(traceback.format_exc())
else:
    app = FastAPI()

    @app.post("/next_steps")
    async def read_root(request: Request):
        payload = await request.json()
        prompt = payload.get("prompt")
        response = await run_conversation_w_prompt(prompt.strip())
        return response