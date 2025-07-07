# Tissue.AI 🤖

Supercharging open source contributions. Paste any GitHub issue URL and our agent analyzes the codebase to provide step-by-step guidance to help newcomers confidently tackle their first contribution.

## Inspiration 💡

One of the biggest barriers for new developers is knowing where to start when contributing to open-source projects. Staring at unfamiliar codebases with hundreds of files can be overwhelming, especially when trying to understand how to fix a specific GitHub issue. We wanted to create an AI-powered tool that bridges this gap by providing newcomers with the context, guidance, and confidence they need to make their first meaningful contribution.

## What It Does 🎯

Our project helps users understand and guide them along the process of fixing GitHub repo issues. The client pastes the link of an issue they're working on, and we use agent orchestration to process the repository and the specific files that the issue targets. Our system collects data persistently through Letta's MemGPT technology and synthesizes information in an interactive and easy-to-grok format for users. The structured and specific data can greatly benefit developers new to the project.

## How We Built It 🛠️

### Frontend:

- **Next.js**: For server-side rendering and routing.
- **React**: For building UI components.
- **Tailwind CSS**: For utility-first styling.
- **Monaco Editor**: For an interactive, IDE-like code viewer.

### Backend:

- **FastAPI**: For building the backend server.
- **Letta & MCP**: To analyze GitHub issues and repositories.
- **Pydantic**: For data validation and schema management.

## Key Features ✨

- **Multi-Agent System**: Utilizes Letta for complex repository analysis.
- **Intuitive UI**: A glassmorphism UI that makes technical information accessible.
- **Scalable Architecture**: Can handle repositories of varying sizes and complexity.
- **Full-Stack Application**: Built from scratch during the hackathon timeframe.

## Getting Started 🚀

### Prerequisites

- Node.js 20+
- Python 3.12+
- uv

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/aaron-ang/tissue-ai.git
   ```
2. **Install frontend dependencies:**
   ```bash
   cd frontend
   npm install
   ```
3. **Install backend dependencies:**
   ```bash
   cd backend
   uv sync
   cp .env.example .env
   ```
   Then, add your `LETTA_API_KEY` to the `.env` file.

### Running the Application

1. **Start the backend server:**
   ```bash
   cd backend
   uv run fastapi dev
   ```
2. **Start the frontend development server:**
   ```bash
   cd ../frontend
   npm run dev
   ```

## Usage 📖

1. Open your browser and navigate to `http://localhost:3000`.
2. Paste a GitHub issue URL into the input field.
3. Click the "Analyze" button.
4. View the analysis, which includes a summary of the issue, project context, and implementation steps.

## What's Next 🔮

- **Interactive Chatbot**: To provide more tailored responses.
- **Multi-Repository Analysis**: To handle issues that span across multiple codebases.
- **Personalized Learning Paths**: To recommend relevant tutorials and concepts.
- **Community Features**: To allow users to share analysis results.
- **IDE Extensions**: To bring Tissue.AI directly into developers' workflows.

## Meet the Team 👋

- [Kai Navratil](https://www.linkedin.com/in/kairi-navratil/)
- [Elizabeth Chen](https://www.linkedin.com/in/elizabeth-c-059762238/)
- [Bode Chiu](https://www.linkedin.com/in/bodechiu/)
- [Aaron Ang](https://www.linkedin.com/in/aaron-ayd/)
