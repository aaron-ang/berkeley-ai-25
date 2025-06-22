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
