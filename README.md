# Naukri AutoAI

**Naukri AutoAI** is an intelligent job application assistant for Naukri.com. It automates repetitive application steps, uses resume-aware AI to answer recruiter questionnaires, and maintains a local response cache to reduce repeated LLM calls.

The project is built with Python, Playwright, LangChain, and Groq. It is designed for local use, with credentials and resume context stored on your machine.

## Key Capabilities

- **Automated application flow**: Opens Naukri recommended jobs, selects suitable listings, and starts the application process.
- **Resume-aware questionnaire handling**: Uses your resume and prompt configuration to answer recruiter questions with relevant responses.
- **LLM-powered decisioning**: Uses Groq through LangChain for reasoning over dynamic questions and available options.
- **Local response cache**: Reuses answers for previously seen questions to reduce latency and API usage.
- **Human-like browser interaction**: Adds realistic typing, scrolling, mouse movement, and timing behavior during browser automation.
- **Run reports**: Generates a JSON and Excel summary of each run — jobs applied, questions answered, and skipped/failed attempts.

## Tech Stack

- Python
- Playwright
- LangChain
- Groq
- SQLite

## Prerequisites

Before running the project, make sure you have:

- Python 3.8 or later
- A Naukri.com account
- A Groq API key
- Chromium installed through Playwright

## Setup

### 1. Create a virtual environment

Windows:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
NAUKRI_EMAIL="your_email@example.com"
NAUKRI_PASSWORD="your_naukri_password"
GROQ_API_KEY="your_groq_api_key"
```

Do not commit `.env` or any credential files.

### 4. Add resume and prompt context

Update the files inside the `data` directory:

- `data/resume.txt`: Plain-text resume used by the AI questionnaire engine.
- `data/system_prompt.txt`: System-level instructions for answer generation.
- `data/human_prompt.txt`: User-level prompt template for questionnaire responses.
- `data/db.json`: Local cache for previously answered recruiter questions.

If `data/db.json` is missing, the application creates it automatically on startup.

## Usage

Start the assistant from the project root:

```bash
python main.py
```

Naukri AutoAI will launch Chromium, sign in to Naukri, open recommended jobs, and process applications based on the configured workflow.

## Project Structure

```text
app/
  ai/              LLM initialization and AI answer generation
  bot/             Browser automation and application workflow
  config/          Environment and runtime configuration
  database/        Database utilities
  repository/      Local response storage helpers
  utils/           File loading, human interaction simulation, parsing, and run reports
data/
  resume.txt       Resume context for AI-generated responses
  system_prompt.txt
  human_prompt.txt
  reports/         Generated per-run JSON/Excel reports (not committed)
main.py            Application entry point
```

## Local Data

The project stores local runtime data for caching and personalization:

- `naukri_autoai_memory.db`: LangChain SQLite cache for repeated LLM requests.
- `data/db.json`: Question-and-answer cache for recruiter questionnaires.
- `data/reports/`: Per-run JSON and Excel reports produced by `app/utils/report.py`.

These files may contain personal or application-specific data and should not be committed.

## Responsible Use

Use this project only with accounts you own and in accordance with the terms and policies of the services involved. Review generated answers before relying on them for important applications, and keep your resume, prompts, credentials, and API keys private.
