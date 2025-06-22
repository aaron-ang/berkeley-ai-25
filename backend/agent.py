import os
import json
from dotenv import load_dotenv

from letta_client import Letta, CreateBlock, MessageCreate

from schema import GitHubIssueAnalysis, IssueSummary, Analysis


load_dotenv()

LETTA_API_KEY = os.getenv("LETTA_API_KEY")


SUPERVISOR_PERSONA = """You are a GitHub Issue Analysis Coordinator specializing in task delegation and result synthesis.

Your primary responsibilities:
- Coordinate analysis of GitHub issues to produce structured JSON output
- Delegate specific tasks to the worker agent for detailed technical investigation
- Synthesize worker findings into a final structured response
- Ensure comprehensive coverage of all relevant files and code sections

For each GitHub issue analysis, you must:
1. First, delegate to the worker to fetch and analyze the GitHub issue details
2. Based on initial findings, delegate further investigation of relevant repositories, files, and code
3. Compile a final JSON response that matches the required schema

The response must include:
- issue_summary: Complete issue details (title, description, labels, status, assignees)
- relevant_files: Directory structure with files, relevance scores, and key code sections
- analysis: Problem type, complexity, approach, dependencies, and test scenarios

Always ensure the final response is valid JSON that matches the expected schema."""

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
    try:
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
        print(f"Added {len(tool_ids)} tools from {mcp_server_name}")
    except Exception as e:
        print(f"Error adding MCP tools from {mcp_server_name}: {e}")
    return tool_ids


def analyze_gh_issue(issue_url: str) -> GitHubIssueAnalysis:
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

    try:
        # Add MCP tools
        mcp_tool_ids = []
        mcp_tool_ids.extend(add_mcp_tools(letta_client, "deepwiki"))
        mcp_tool_ids.extend(add_mcp_tools(letta_client, "github"))

        # Create shared memory block with analysis context
        shared_block = letta_client.blocks.create(
            value=f"GitHub Issue Analysis Session\nTarget: {issue_url}\nObjective: Extract structured data for issue resolution",
            label="analysis_session",
        )

        # Create supervisor agent - coordinates and synthesizes
        supervisor = letta_client.agents.create(
            name="github-issue-supervisor",
            memory_blocks=[
                CreateBlock(label="persona", value=SUPERVISOR_PERSONA),
                CreateBlock(
                    label="human",
                    value="User needs structured JSON analysis of GitHub issues including relevant files and code sections.",
                ),
                CreateBlock(
                    label="output_format",
                    value="Must produce valid JSON that matches the GitHubIssueAnalysis schema with issue_summary, relevant_files, and analysis sections.",
                    description="Defines the required JSON output structure for issue analysis",
                ),
            ],
            tools=["send_message_to_agents_matching_tags"],
            tool_ids=mcp_tool_ids,
            block_ids=[shared_block.id],
            model="anthropic/claude-opus-4-20250514",
            embedding="openai/text-embedding-3-small",
            response_format={"json_schema": GitHubIssueAnalysis.model_json_schema()},
        )
        print(f"Created supervisor agent: {supervisor.id}")

        # Create worker agent - does detailed technical analysis
        worker = letta_client.agents.create(
            name="github-issue-worker",
            memory_blocks=[
                CreateBlock(label="persona", value=WORKER_PERSONA),
                CreateBlock(
                    label="human",
                    value="User requires detailed GitHub technical analysis. I work with supervisor to extract structured data.",
                ),
                CreateBlock(
                    label="analysis_guidelines",
                    value="Focus on extracting: file paths, line numbers, code sections, relevance scores, and technical insights.",
                    description="Guidelines for conducting thorough technical analysis of GitHub repositories",
                ),
            ],
            tools=["send_message_to_agents_matching_tags"],
            tool_ids=mcp_tool_ids,
            block_ids=[shared_block.id],
            model="gemini-key/gemini-2.5-flash-preview-05-20",
            embedding="google_ai/gemini-embedding-exp-03-07",
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

Coordinate with the worker agent to gather detailed technical information, then compile everything into the required JSON format. The response must be valid JSON that matches the GitHubIssueAnalysis schema.""",
                )
            ],
        )

        # Extract the final JSON response
        analysis_result = None
        for message in response.messages:
            if message.message_type == "assistant_message":
                print(f"Supervisor response: {message.content}")
                # Try to parse the JSON response
                try:
                    content = message.content
                    if "```json" in content:
                        # Extract JSON from code block
                        json_start = content.find("```json") + 7
                        json_end = content.find("```", json_start)
                        json_content = content[json_start:json_end].strip()
                        parsed_data = json.loads(json_content)
                    elif content.strip().startswith("{"):
                        # Try to parse the entire content as JSON
                        parsed_data = json.loads(content)
                    else:
                        # Content might be raw JSON
                        parsed_data = json.loads(content)

                    # Validate with Pydantic
                    analysis_result = GitHubIssueAnalysis(**parsed_data)

                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON from response: {e}")
                    # Create fallback structure
                    analysis_result = GitHubIssueAnalysis(
                        issue_summary=IssueSummary(
                            title="Analysis in progress",
                            description="Could not parse complete analysis",
                            status="unknown",
                        ),
                        relevant_files={},
                        analysis=Analysis(
                            problem_type="unknown",
                            complexity="unknown",
                            suggested_approach=content[:500] + "..."
                            if len(content) > 500
                            else content,
                        ),
                    )
                except Exception as e:
                    print(f"Error validating with Pydantic: {e}")
                    # Create fallback structure
                    analysis_result = GitHubIssueAnalysis(
                        issue_summary=IssueSummary(
                            title="Validation error",
                            description="Response did not match expected schema",
                            status="unknown",
                        ),
                        relevant_files={},
                        analysis=Analysis(
                            problem_type="unknown",
                            complexity="unknown",
                            suggested_approach="Schema validation failed",
                        ),
                    )
            elif message.message_type == "tool_call_message":
                print(f"Tool called: {message.tool_call.name}")
            elif message.message_type == "tool_return_message":
                print(f"Tool result preview: {str(message.tool_return)[:200]}...")

        if not analysis_result:
            # Fallback response structure
            analysis_result = GitHubIssueAnalysis(
                issue_summary=IssueSummary(
                    title="Analysis incomplete",
                    description="Could not complete full analysis",
                    status="unknown",
                ),
                relevant_files={},
                analysis=Analysis(
                    problem_type="unknown",
                    complexity="unknown",
                    suggested_approach="Manual analysis required",
                ),
            )

        return analysis_result

    except Exception as e:
        print(f"Error during analysis: {e}")
        raise


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
