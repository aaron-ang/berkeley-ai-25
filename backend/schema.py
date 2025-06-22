from typing import List, Dict, Optional

from pydantic import BaseModel, Field


class KeySection(BaseModel):
    line_start: int = Field(description="Starting line number")
    line_end: int = Field(description="Ending line number")
    code: str = Field(description="Code content from specified lines")
    explanation: str = Field(description="Why these lines are relevant to the issue")


class FileInfo(BaseModel):
    type: str = Field(description="'file' or 'directory'")
    reason: Optional[str] = Field(default=None, description="Why this file is relevant")
    key_sections: Optional[List[KeySection]] = Field(
        default=[], description="Key code sections"
    )
    files: Optional[Dict[str, "FileInfo"]] = Field(
        default=None, description="Nested files for directories"
    )


class ProjectContext(BaseModel):
    overview: str = Field(description="High-level overview of what the project does")
    architecture_overview: str = Field(
        description="Explanation of the overall project architecture and component relationships"
    )
    main_directories: Dict[str, str] = Field(
        default={}, description="Key directories and their purposes"
    )


class BuildAndTest(BaseModel):
    setup_commands: List[str] = Field(
        default=[], description="Commands to set up the development environment"
    )
    build_commands: List[str] = Field(
        default=[], description="Commands to build the project"
    )
    test_commands: List[str] = Field(default=[], description="Commands to run tests")
    lint_commands: List[str] = Field(
        default=[], description="Commands to run linting/code style checks"
    )
    development_server: Optional[str] = Field(
        default=None, description="Command to start the development server"
    )
    environment_requirements: List[str] = Field(
        default=[], description="Required environment variables or configuration"
    )


class IssueSummary(BaseModel):
    title: str = Field(description="Title of the GitHub issue")
    description: str = Field(description="Brief description of the issue")
    labels: List[str] = Field(
        default=[], description="Labels associated with the issue"
    )
    status: str = Field(description="Current status of the issue (open/closed)")


class Analysis(BaseModel):
    problem_type: str = Field(description="Type of problem (bug/feature/enhancement)")
    complexity: str = Field(description="Complexity level (low/medium/high)")
    affected_components: List[str] = Field(
        default=[], description="Project components affected by this issue"
    )
    implementation_steps: List[str] = Field(
        default=[], description="Steps to implement the solution"
    )
    dependencies: List[str] = Field(
        default=[], description="List of related files/components"
    )
    tests_needed: List[str] = Field(default=[], description="Suggested test scenarios")
    potential_risks: List[str] = Field(
        default=[], description="Potential risks or side effects to consider"
    )
    related_documentation: List[str] = Field(
        default=[], description="Relevant documentation files or external resources"
    )


class GitHubIssueAnalysis(BaseModel):
    issue_summary: IssueSummary = Field(description="GitHub issue summary")
    project_context: ProjectContext = Field(
        description="Project context for new contributors"
    )
    relevant_files: Dict[str, FileInfo] = Field(
        description="Relevant files and directories with structure"
    )
    build_and_test: BuildAndTest = Field(description="Build, test, and dev commands")
    analysis: Analysis = Field(description="Technical analysis and recommendations")


# Allow forward references for recursive FileInfo model
FileInfo.model_rebuild()


def create_mock_analysis():
    """Create mock analysis data for testing purposes."""
    return GitHubIssueAnalysis(
        issue_summary=IssueSummary(
            title="Fix authentication bug in user login flow",
            description="Users experiencing intermittent authentication failures with OAuth providers. Issue appears related to token validation in backend service.",
            labels=["bug", "authentication", "high-priority"],
            status="open",
        ),
        project_context=ProjectContext(
            overview="Microservice-based authentication system handling user login, registration, and OAuth integration",
            architecture_overview="Layered architecture with API endpoints, auth logic, data models, and middleware. OAuth providers integrate through callback handlers with JWT validation.",
            main_directories={
                "src/": "Main application source code",
                "src/auth/": "Authentication and authorization logic",
                "src/models/": "Database models and schemas",
                "src/api/": "REST API endpoints",
                "tests/": "Unit and integration tests",
                "config/": "Configuration and environment settings",
            },
        ),
        relevant_files={
            "src": FileInfo(
                type="directory",
                reason="Main source directory with authentication logic",
                architecture_role="Root directory with all application logic by functional modules",
                files={
                    "auth": FileInfo(
                        type="directory",
                        reason="Authentication module with buggy OAuth implementation",
                        architecture_role="Core auth module handling OAuth flows and token validation",
                        dependencies=["src/models/user.py", "config/settings.py"],
                        dependents=["src/api/auth_routes.py", "src/middleware.py"],
                        files={
                            "oauth.py": FileInfo(
                                type="file",
                                reason="Contains OAuth token validation causing intermittent failures",
                                architecture_role="Handles OAuth integration, token exchange, and validation",
                                dependencies=["jwt", "src/models/user.py"],
                                dependents=["src/api/auth_routes.py"],
                                key_sections=[
                                    KeySection(
                                        line_start=45,
                                        line_end=62,
                                        code="def validate_token(token: str) -> bool:\n    try:\n        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])\n        return True\n    except jwt.ExpiredSignatureError:\n        return False",
                                        explanation="Token validation with potential race condition issues",
                                    ),
                                ],
                            ),
                        },
                    ),
                },
            ),
        },
        build_and_test=BuildAndTest(
            setup_commands=[
                "python -m venv venv",
                "source venv/bin/activate",
                "pip install -r requirements.txt",
                "docker-compose up -d",
            ],
            build_commands=["python -m pip install -e .", "alembic upgrade head"],
            test_commands=["pytest tests/", "pytest tests/test_auth.py -v"],
            lint_commands=["black src/ tests/", "flake8 src/"],
            development_server="uvicorn src.main:app --reload --port 8000",
            environment_requirements=[
                "DATABASE_URL (PostgreSQL connection)",
                "REDIS_URL (Redis connection)",
                "JWT_SECRET_KEY (token signing)",
                "OAUTH_CLIENT_ID and OAUTH_CLIENT_SECRET",
            ],
        ),
        analysis=Analysis(
            problem_type="bug",
            complexity="medium",
            affected_components=["OAuth authentication flow", "Token validation"],
            implementation_steps=[
                "Add thread-safe token validation with locking",
                "Implement Redis token caching",
                "Add comprehensive logging",
                "Create concurrent authentication stress tests",
            ],
            dependencies=["src/auth/oauth.py", "JWT library", "Redis session store"],
            tests_needed=[
                "Concurrent login stress test",
                "Token expiration edge cases",
                "OAuth provider timeout handling",
            ],
            potential_risks=[
                "Changes could affect existing user sessions",
                "OAuth provider rate limiting during testing",
            ],
            related_documentation=[
                "docs/authentication.md",
                "README.md",
                "OAuth 2.0 RFC 6749",
            ],
        ),
    )
