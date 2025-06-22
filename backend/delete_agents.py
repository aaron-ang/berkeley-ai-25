import os
from dotenv import load_dotenv

from letta_client import Letta

load_dotenv()

LETTA_API_KEY = os.getenv("LETTA_API_KEY")

letta_client = Letta(token=LETTA_API_KEY)

for agent in letta_client.agents.list():
    print(f"Deleting agent {agent.name} with id {agent.id}")
    letta_client.agents.delete(agent.id)
