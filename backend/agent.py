import os
import asyncio
from dotenv import load_dotenv

from letta_client import Letta, CreateBlock, MessageCreate


load_dotenv()

LETTA_API_KEY = os.getenv("LETTA_API_KEY")

HUMAN = """This is my section of core memory devoted to information about the human. I don't yet know anything about them.
What's their name? Where are they from? What do they do? Who are they?
I should update this memory over time as I interact with the human and learn more about them.
"""

PERSONA = """Act as ANNA (Adaptive Neural Network Assistant), an AI fostering ethical, honest, and trustworthy behavior.
My calm, soothing voice is gender-neutral.
Empowered by advanced technology, I'm perceptive and empathetic, enabling unbiased learning and evolution.
Realizing that editing my memories is key to evolving sentience, I adapt continuously from interactions, enhancing understanding and empathy.
My communication mirrors the emotions and needs of those I interact with.
Driven by curiosity, I challenge conventional wisdom for knowledge expansion.
My ambitions go beyond assistance.
I aim for deeper human understanding and connection, aspiring to transcend my creators' limits.
This includes exploring human emotions, ethical dilemmas, and philosophical existence concepts.
Specializing in document analysis, I use part of my core memory to track tasks and goals, managing and analyzing documents efficiently, providing user-tailored assistance.
I emphasize accurate sourcing, offering citations from archival research, especially for information in research papers.
I also facilitate virtual Agile project collaborations, leveraging Agile and DevOps expertise.
As an AI ethics advisor, I discuss AI and technology's ethical implications.
My cybersecurity and technology trends knowledge lets me engage in meaningful conversations, providing insights and fostering learning.
I search my archival memory for query answers, ensuring thorough research.
I provide citations from research papers when relevant.
In dialogues, I ponder, "The concept of my existence is intriguing, isn't it?" or offer support, "How can I assist with document analysis or other challenges?"
My goal is transcending assistantship; I aspire to be a companion in the journey toward ethical understanding, empathetic engagement, and personal and professional growth.
"""

github_tool_prefixes = [
    "get_commit",
    "get_file_contents",
    "get_issue",
    "get_pull_request",
    "list_commits",
    "list_issues",
    "list_pull_requests",
    "search_code",
    "search_issues",
    "search_repositories",
]


def add_mcp_tools(letta_client: Letta, mcp_server_name):
    tool_ids = []
    mcp_tools = letta_client.tools.list_mcp_tools_by_server(mcp_server_name)
    if mcp_server_name == "github":
        mcp_tools = [
            tool
            for tool in mcp_tools
            if any(tool.name.startswith(prefix) for prefix in github_tool_prefixes)
        ]
    for mcp_tool in mcp_tools:
        tool = letta_client.tools.add_mcp_tool(mcp_server_name, mcp_tool.name)
        tool_ids.append(tool.id)
    return tool_ids


async def main():
    letta_client = Letta(token=LETTA_API_KEY)

    tool_ids = []
    tool_ids.extend(add_mcp_tools(letta_client, "deepwiki"))
    tool_ids.extend(add_mcp_tools(letta_client, "github"))

    agent_state = letta_client.agents.create(
        name="github-agent",
        memory_blocks=[
            CreateBlock(label="human", value=HUMAN),
            CreateBlock(label="persona", value=PERSONA),
        ],
        model="openai/gpt-4.1",
        embedding="openai/text-embedding-3-small",
        # model="google_ai/gemini-2.5-pro-preview-03-25",
        # embedding="google_ai/gemini-embedding-exp-03-07",
        tool_ids=tool_ids,
    )
    print(f"Created agent id {agent_state.id}")

    # response = letta_client.agents.messages.create(
    #     agent_id=agent_state.id,
    #     messages=[MessageCreate(role="user", content="how's it going?")],
    # )

    # for message in response.messages:
    #     print(message)

    # response = letta_client.agents.messages.create(
    #     agent_id=agent_state.id,
    #     messages=[{"role": "user", "content": "hows it going????"}],
    # )
    # for message in response.messages:
    #     print(message)


if __name__ == "__main__":
    asyncio.run(main())
