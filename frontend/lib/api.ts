import axios from 'axios';

// API configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Types for the API response
export interface KeySection {
  line_start: number;
  line_end: number;
  code: string;
  explanation: string;
}

export interface FileInfo {
  type: 'file' | 'directory';
  relevance_score?: number;
  reason?: string;
  key_sections?: KeySection[];
  files?: { [key: string]: FileInfo };
}

export interface IssueSummary {
  title: string;
  description: string;
  labels: string[];
  status: string;
  assignees: string[];
}

export interface Analysis {
  problem_type: string;
  complexity: string;
  suggested_approach: string;
  dependencies: string[];
  tests_needed: string[];
}

export interface GitHubIssueAnalysis {
  issue_summary: IssueSummary;
  relevant_files: { [key: string]: FileInfo };
  analysis: Analysis;
}

// Flattened file structure for display
export interface FlattenedFile {
  pathName: string;
  reason: string;
  keySections: KeySection[];
}

// Function to flatten the relevant_files structure
export function flattenRelevantFiles(relevantFiles: { [key: string]: FileInfo }, basePath: string = ''): FlattenedFile[] {
  const flattened: FlattenedFile[] = [];

  for (const [fileName, fileInfo] of Object.entries(relevantFiles)) {
    const currentPath = basePath ? `${basePath}/${fileName}` : fileName;

    // Only include files (not directories) with a reason
    if (fileInfo.type === 'file' && fileInfo.reason) {
      flattened.push({
        pathName: currentPath,
        reason: fileInfo.reason,
        keySections: fileInfo.key_sections || []
      });
    }

    // Recursively process nested files if this is a directory
    if (fileInfo.type === 'directory' && fileInfo.files) {
      const nestedFiles = flattenRelevantFiles(fileInfo.files, currentPath);
      flattened.push(...nestedFiles);
    }
  }

  return flattened;
}

// API function to analyze GitHub issue
export async function analyzeGitHubIssue(githubUrl: string): Promise<{
  analysis: GitHubIssueAnalysis;
  flattenedFiles: FlattenedFile[];
}> {
  try {
    const response = await api.post('/analyze', {
      github_url: githubUrl
    });

    const analysis: GitHubIssueAnalysis = response.data;
    const flattenedFiles = flattenRelevantFiles(analysis.relevant_files);

    return {
      analysis,
      flattenedFiles
    };
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(`API Error: ${error.response?.data?.detail || error.message}`);
    }
    throw new Error(`Unexpected error: ${error}`);
  }
}
