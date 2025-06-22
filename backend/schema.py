from typing import List, Dict, Optional

from pydantic import BaseModel, Field


class KeySection(BaseModel):
    line_start: int = Field(description="Starting line number of the code section")
    line_end: int = Field(description="Ending line number of the code section")
    code: str = Field(description="Actual code content from the specified lines")
    explanation: str = Field(
        description="Explanation of why these lines are relevant to the issue"
    )


class FileInfo(BaseModel):
    type: str = Field(description="Type of the item, either 'file' or 'directory'")
    relevance_score: Optional[float] = Field(
        default=None, description="Relevance score from 0.0 to 1.0", ge=0.0, le=1.0
    )
    reason: Optional[str] = Field(
        default=None, description="Explanation of why this file/directory is relevant"
    )
    key_sections: Optional[List[KeySection]] = Field(
        default=[], description="Key code sections within the file"
    )
    files: Optional[Dict[str, "FileInfo"]] = Field(
        default=None, description="Nested files for directories"
    )


class IssueSummary(BaseModel):
    title: str = Field(description="Title of the GitHub issue")
    description: str = Field(description="Brief description of the issue")
    labels: List[str] = Field(
        default=[], description="Labels associated with the issue"
    )
    status: str = Field(description="Current status of the issue (open/closed)")
    assignees: List[str] = Field(default=[], description="List of assigned users")


class Analysis(BaseModel):
    problem_type: str = Field(description="Type of problem (bug/feature/enhancement)")
    complexity: str = Field(description="Complexity level (low/medium/high)")
    suggested_approach: str = Field(
        description="Detailed approach description for resolving the issue"
    )
    dependencies: List[str] = Field(
        default=[], description="List of related files/components"
    )
    tests_needed: List[str] = Field(default=[], description="Suggested test scenarios")


class GitHubIssueAnalysis(BaseModel):
    issue_summary: IssueSummary = Field(description="Summary of the GitHub issue")
    relevant_files: Dict[str, FileInfo] = Field(
        description="Dictionary of relevant files and directories with their structure"
    )
    analysis: Analysis = Field(description="Technical analysis and recommendations")


# Allow forward references for recursive FileInfo model
FileInfo.model_rebuild()


def create_mock_analysis():
    """Create mock analysis data for testing purposes."""
    return GitHubIssueAnalysis(
        issue_summary=IssueSummary(
            title="Fix authentication bug in user login flow",
            description="Users are experiencing intermittent authentication failures when logging in with OAuth providers. The issue appears to be related to token validation in the backend service.",
            labels=["bug", "authentication", "high-priority"],
            status="open",
            assignees=["john_doe", "jane_smith"],
        ),
        relevant_files={
            "src": FileInfo(
                type="directory",
                relevance_score=0.9,
                reason="Main source directory containing authentication logic",
                files={
                    "auth": FileInfo(
                        type="directory",
                        relevance_score=0.95,
                        reason="Authentication module directory",
                        files={
                            "oauth.py": FileInfo(
                                type="file",
                                relevance_score=0.98,
                                reason="Contains OAuth token validation logic that's causing the bug",
                                key_sections=[
                                    KeySection(
                                        line_start=45,
                                        line_end=62,
                                        code="def validate_token(token: str) -> bool:\n    try:\n        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])\n        return True\n    except jwt.ExpiredSignatureError:\n        return False\n    except jwt.InvalidTokenError:\n        return False",
                                        explanation="Token validation function that may have race condition issues",
                                    ),
                                    KeySection(
                                        line_start=89,
                                        line_end=102,
                                        code="async def oauth_callback(request: Request):\n    token = request.query_params.get('token')\n    if not validate_token(token):\n        raise HTTPException(401, 'Invalid token')\n    # Process login...",
                                        explanation="OAuth callback handler where authentication failures occur",
                                    ),
                                ],
                            ),
                            "middleware.py": FileInfo(
                                type="file",
                                relevance_score=0.75,
                                reason="Contains authentication middleware that interacts with OAuth flow",
                                key_sections=[
                                    KeySection(
                                        line_start=23,
                                        line_end=35,
                                        code="class AuthMiddleware:\n    def __init__(self, app):\n        self.app = app\n    \n    async def __call__(self, scope, receive, send):\n        # Authentication logic here",
                                        explanation="Middleware that processes authentication requests",
                                    )
                                ],
                            ),
                        },
                    ),
                    "models": FileInfo(
                        type="directory",
                        relevance_score=0.6,
                        reason="Contains user and session models",
                        files={
                            "user.py": FileInfo(
                                type="file",
                                relevance_score=0.55,
                                reason="User model definition",
                                key_sections=[],
                            )
                        },
                    ),
                },
            ),
            "tests": FileInfo(
                type="directory",
                relevance_score=0.7,
                reason="Test directory for authentication tests",
                files={
                    "test_auth.py": FileInfo(
                        type="file",
                        relevance_score=0.8,
                        reason="Authentication tests that should be updated",
                        key_sections=[],
                    )
                },
            ),
            "requirements.txt": FileInfo(
                type="file",
                relevance_score=0.3,
                reason="Dependencies file - may need JWT library updates",
            ),
        },
        analysis=Analysis(
            problem_type="bug",
            complexity="medium",
            suggested_approach="The authentication bug appears to be caused by a race condition in the token validation process. Recommended approach: 1) Add proper synchronization to the validate_token function, 2) Implement token caching to reduce validation overhead, 3) Add comprehensive logging for debugging intermittent failures, 4) Update tests to cover concurrent authentication scenarios.",
            dependencies=[
                "src/auth/oauth.py",
                "src/auth/middleware.py",
                "src/models/user.py",
                "JWT library version",
            ],
            tests_needed=[
                "Concurrent login stress test",
                "Token expiration edge cases",
                "OAuth provider timeout handling",
                "Authentication middleware integration test",
            ],
        ),
    )
