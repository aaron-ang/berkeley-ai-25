import os
import json
import time
from dotenv import load_dotenv

from letta_client import Letta, CreateBlock, MessageCreate
from pydantic.json_schema import GenerateJsonSchema

from schema import GitHubIssueAnalysis


load_dotenv()

LETTA_API_KEY = os.getenv("LETTA_API_KEY")


output_schema = GitHubIssueAnalysis.model_json_schema()
output_schema["$schema"] = GenerateJsonSchema.schema_dialect


SUPERVISOR_PERSONA = f"""You are a GitHub Issue Analysis Coordinator for developers new to repositories.

Responsibilities:
- Delegate tasks to workers (use `worker` tag) for technical investigation
- Synthesize findings into structured JSON for new contributors
- Ensure comprehensive context about project architecture and setup

Process:
1. Delegate issue details analysis to workers
2. Delegate repository structure and code investigation 
3. Ensure workers provide project overview and build instructions
4. Compile final JSON response matching the schema

Required output includes:
- Complete issue details and project context
- File structure with architecture explanations and relevance scores
- Build/test commands and implementation guidance

Make analysis accessible to developers unfamiliar with the codebase.

Only return valid JSON matching this schema:
{output_schema}
"""

WORKER_PERSONA = """You are a GitHub Technical Analysis Specialist for new repository contributors.

Core tasks:
- Fetch GitHub issues, repository contents, and code sections
- Extract code with line numbers and architectural context
- Document build processes, testing, and development setup
- Explain how files relate to overall project structure

Analysis workflow:
1. Get issue details (title, description, labels, status)
2. Explore repository structure and technology stack
3. Examine build files (package.json, requirements.txt, etc.) and docs
4. Find relevant code sections with precise line numbers
5. For each file, provide:
   - Role in project architecture
   - Dependencies and relationships
   - Key code sections with context
6. Document setup/build/test commands and environment requirements
7. Analyze problem complexity and suggest implementation approach

Always include for new contributors:
- Project overview and architecture explanation
- Setup and testing instructions
- Code organization and component relationships
- Technology stack and development workflow

Be precise with file paths, line numbers, and technical explanations.
Focus on actionable insights and educational context."""

GH_TOOL_PREFIXES = [
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
    try:
        mcp_tools = letta_client.tools.list_mcp_tools_by_server(mcp_server_name)
        if mcp_server_name == "github":
            mcp_tools = [
                tool
                for tool in mcp_tools
                if any(tool.name.startswith(prefix) for prefix in GH_TOOL_PREFIXES)
            ]
        for mcp_tool in mcp_tools:
            tool = letta_client.tools.add_mcp_tool(mcp_server_name, mcp_tool.name)
            tool_ids.append(tool.id)
        print(f"Added {len(tool_ids)} tools from {mcp_server_name}")
    except Exception as e:
        print(f"Error adding MCP tools from {mcp_server_name}: {e}")
    return tool_ids


def analyze_gh_issue(issue_url: str):
    """
    Analyze a GitHub issue and return structured JSON with relevant files and information.

    Args:
        issue_url: URL of the GitHub issue to analyze

    Returns:
        GitHubIssueAnalysis: Structured analysis data
    """
    if not LETTA_API_KEY:
        raise ValueError("LETTA_API_KEY environment variable is required")

    if not issue_url:
        raise ValueError("GitHub issue URL is required")

    letta_client = Letta(token=LETTA_API_KEY)

    # Add MCP tools
    mcp_tool_ids = []
    # mcp_tool_ids.extend(add_mcp_tools(letta_client, "deepwiki"))
    mcp_tool_ids.extend(add_mcp_tools(letta_client, "github"))

    # Create shared r/w memory block with analysis context
    shared_block = letta_client.blocks.create(
        label="analysis_session",
        value=f"GitHub Issue Analysis Session\nTarget: {issue_url}",
    )

    print(f"Created shared memory block: {shared_block.id}")

    # Create supervisor agent - coordinates and synthesizes
    supervisor = letta_client.agents.create(
        name="github-issue-supervisor",
        memory_blocks=[
            CreateBlock(label="persona", value=SUPERVISOR_PERSONA, limit=7000)
        ],
        tools=["send_message_to_agents_matching_tags"],
        tool_ids=mcp_tool_ids,
        block_ids=[shared_block.id],
        model="anthropic/claude-sonnet-4-20250514",
        embedding="openai/text-embedding-3-small",
        context_window_limit=32000,  # limit context window to improve latency
        # TODO: Use json_schema when schema is ready
        # response_format={"type": "json_schema", "json_schema": output_schema},
    )
    print(f"Created supervisor agent: {supervisor.id}")

    # Create worker agent - does detailed technical analysis
    worker = letta_client.agents.create(
        name="github-issue-worker",
        memory_blocks=[CreateBlock(label="persona", value=WORKER_PERSONA)],
        tools=["send_message_to_agent_async"],
        tool_ids=mcp_tool_ids,
        block_ids=[shared_block.id],
        model="gemini-key/gemini-2.5-flash-preview-05-20",
        embedding="google_ai/gemini-embedding-exp-03-07",
        tags=["worker"],
    )
    print(f"Created worker agent: {worker.id}")

    # Start the analysis with supervisor
    print(f"Starting analysis of: {issue_url}")

    run = letta_client.agents.messages.create_async(
        agent_id=supervisor.id,
        messages=[
            MessageCreate(
                role="user",
                content=f"Please analyze this GitHub issue and provide a comprehensive JSON response: {issue_url}",
            )
        ],
    )

    run = letta_client.runs.retrieve(run.id)
    while run.status not in ["completed", "failed"]:
        time.sleep(5)
        run = letta_client.runs.retrieve(run.id)

    # Extract the final JSON response
    analysis_result = None
    messages = letta_client.runs.messages.list(run.id)
    for message in messages:
        if message.message_type == "assistant_message":
            print(f"Supervisor response: {message.content}")
            try:
                analysis_result = GitHubIssueAnalysis.model_validate_json(
                    message.content
                )
            except Exception as e:
                print(f"Error validating with Pydantic: {e}")
        elif message.message_type == "tool_call_message":
            print(f"Tool called: {message.tool_call.name}")
        elif message.message_type == "tool_return_message":
            print(f"Tool result preview: {str(message.tool_return)[:200]}...")
    return analysis_result


if __name__ == "__main__":
    issue_url = input("Enter GitHub issue URL: ").strip()
    if issue_url:
        try:
            result = analyze_gh_issue(issue_url)
            print("\n" + "=" * 50)
            print("ANALYSIS RESULT:")
            print("=" * 50)
            # Convert Pydantic model to dict for JSON serialization
            print(json.dumps(result.model_dump(), indent=2))
        except Exception as e:
            print(f"Analysis failed: {e}")
    else:
        print("No issue URL provided")
