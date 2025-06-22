import os
from dotenv import load_dotenv

from letta_client import Letta

load_dotenv()

LETTA_API_KEY = os.getenv("LETTA_API_KEY")

letta_client = Letta(token=LETTA_API_KEY)

for agent in letta_client.agents.list():
    # Keep this agent for testing purposes
    if agent.id in [
        "agent-d234d3b9-6dd2-4e8d-930a-8111163704fb",
        "agent-9431f02a-d92a-4e64-971e-130a5cad8187",
    ]:
        continue

    print(f"Deleting agent {agent.name} with id {agent.id}")
    letta_client.agents.delete(agent.id)
