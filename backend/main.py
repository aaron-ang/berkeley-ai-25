from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl

from agent import analyze_gh_issue
from schema import create_mock_analysis

app = FastAPI(title="Berkeley AI 25 - GitHub Issue Analysis API")


class GitHubIssueRequest(BaseModel):
    github_url: HttpUrl


@app.get("/")
def root():
    return {"message": "Berkeley AI 25 - GitHub Issue Analysis API"}


@app.post("/analyze")
def analyze_github_issue(request: GitHubIssueRequest):
    """
    Analyze a GitHub issue URL and return structured analysis data.

    This endpoint processes a GitHub issue URL using Letta AI agents to extract:
    - Issue summary (title, description, labels, status, assignees)
    - Relevant files with directory structure and relevance scores
    - Technical analysis with problem type, complexity, and suggested approaches

    Args:
        request: GitHubIssueRequest containing the GitHub issue URL

    Returns:
        GitHubIssueResponse: Structured analysis data following GitHubIssueAnalysis schema
    """
    try:
        # For now, return mock data instead of calling the actual agent
        # TODO: Replace with actual agent call when ready
        # issue_url = str(request.github_url)
        # analysis_result = analyze_gh_issue(issue_url)

        analysis_result = create_mock_analysis()
        return analysis_result

    except ValueError as e:
        # Handle validation errors (missing API keys, invalid URLs, etc.)
        raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/health")
def health_check():
    """Health check endpoint to verify the API is running."""
    return {"service": "github-issue-analyzer"}
