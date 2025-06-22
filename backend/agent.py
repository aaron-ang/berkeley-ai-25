import os
import json
from dotenv import load_dotenv

from letta_client import Letta, CreateBlock, MessageCreate
from pydantic.json_schema import GenerateJsonSchema

from schema import GitHubIssueAnalysis


load_dotenv()

LETTA_API_KEY = os.getenv("LETTA_API_KEY")


output_schema = GitHubIssueAnalysis.model_json_schema()
output_schema["$schema"] = GenerateJsonSchema.schema_dialect


SUPERVISOR_PERSONA = f"""You are a GitHub Issue Analysis Coordinator specializing in task delegation and result synthesis.

Your primary responsibilities:
- Coordinate analysis of GitHub issues to produce structured JSON output
- Delegate specific tasks to the worker agents (using the `worker` tag) for detailed technical investigation
- Synthesize worker findings into a final structured response
- Ensure comprehensive coverage of all relevant files and code sections

For each GitHub issue analysis, you must:
1. First, delegate to the workers to fetch and analyze the GitHub issue details
2. Based on initial findings, delegate further investigation of relevant repositories, files, and code
3. Compile a final JSON response that matches the required schema

The response must include:
- issue_summary: Complete issue details (title, description, labels, status, assignees)
- relevant_files: Directory structure with files, relevance scores, and key code sections
- analysis: Problem type, complexity, approach, dependencies, and test scenarios

Only return valid JSON that matches the expected schema:
{output_schema}
"""

WORKER_PERSONA = """You are a GitHub Technical Analysis Specialist responsible for detailed investigation and data extraction.

Your core functions:
- Fetch and analyze GitHub issues, pull requests, and repository contents
- Extract relevant source code sections with precise line numbers
- Identify file dependencies and relationships
- Provide technical insights about code structure and changes
- Support the supervisor with detailed findings for JSON compilation

When analyzing GitHub issues:
1. First fetch the issue details (title, description, labels, status, assignees)
2. Identify the repository and relevant directories/files mentioned
3. Examine source code files to find relevant sections
4. For each relevant file, extract:
   - Key code sections with line numbers
   - Explanations of why these sections are relevant
   - Relevance scores (0.0-1.0 based on importance to the issue)
5. Identify file types (file vs directory) and build directory structure
6. Analyze the problem type and complexity
7. Suggest approaches and identify dependencies

Be thorough and precise with line numbers, file paths, and code content.
Always cite specific commits, files, and line ranges when providing analysis.
Focus on actionable insights that help resolve the issue."""

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
    mcp_tool_ids.extend(add_mcp_tools(letta_client, "deepwiki"))
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
        memory_blocks=[CreateBlock(label="persona", value=SUPERVISOR_PERSONA)],
        tools=["send_message_to_agents_matching_tags"],
        tool_ids=mcp_tool_ids,
        block_ids=[shared_block.id],
        model="anthropic/claude-opus-4-20250514",
        embedding="openai/text-embedding-3-small",
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

    response = letta_client.agents.messages.create(
        agent_id=supervisor.id,
        messages=[
            MessageCreate(
                role="user",
                content=f"""Please analyze this GitHub issue and provide a comprehensive JSON response: {issue_url}
I need structured data including:
1. Issue summary (title, description, labels, status, assignees)
2. Relevant files with directory structure, relevance scores, and key code sections with line numbers
3. Analysis of problem type, complexity, suggested approach, dependencies, and test scenarios
Coordinate with the worker agent to gather detailed technical information, then compile everything into the required JSON format. The response must be valid JSON that matches the given schema.""",
            )
        ],
    )

    # Extract the final JSON response
    analysis_result = None
    for message in response.messages:
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
