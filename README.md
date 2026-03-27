# OS-APOW: Orchestrator for Sentinel, Planning, and Orchestration Workflows

[![Repository Summary](.ai-repository-summary.md)](.ai-repository-summary.md)

## Overview

This is an **Autonomous AI Orchestration System** that transforms GitHub Issues into execution orders fulfilled by specialized AI agents without human intervention. The system follows a "Self-Bootstrapping" philosophy where it can build and evolve itself using its own orchestration capabilities.

## Core Components

- **Work Event Notifier ("The Ear")** - FastAPI-based webhook receiver for GitHub events
- **Work Queue ("The Logic State")** - GitHub-backed distributed state management using labels
- **Sentinel Orchestrator ("The Brain")** - Persistent supervisor managing worker lifecycle
- **Opencode Worker ("The Hands")** - Agentic execution environment

## Technology Stack

- **Python 3.12+** with FastAPI async web framework
- **uv** for high-speed package management
- **Pydantic** for strict schema validation
- **httpx** for async HTTP client with connection pooling
- **Docker/DevContainer** for containerization

## Project Structure

```
src/orchestrator/
├── __init__.py           # Package initialization
├── main.py               # FastAPI application entry point
├── api/
│   ├── __init__.py
│   └── routes.py         # API routes (health, readiness)
├── models/
│   ├── __init__.py
│   └── work_item.py      # WorkItem, TaskType, WorkItemStatus
├── queue/
│   ├── __init__.py
│   └── github_queue.py   # GitHub-backed work queue
└── services/
    ├── __init__.py
    ├── sentinel.py       # Sentinel orchestrator service
    └── notifier.py       # Webhook receiver service

tests/
├── __init__.py
├── conftest.py           # Pytest fixtures
└── test_main.py          # API tests
```

## Development Setup

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

```bash
# Install dependencies
uv sync

# Install dev dependencies
uv sync --extra dev
```

### Running the Services

```bash
# Run the main orchestrator API
uv run orchestrator

# Run the sentinel service
uv run sentinel

# Run the notifier service
uv run notifier
```

### Development Commands

```bash
# Run tests
uv run pytest

# Run linting
uv run ruff check src/ tests/

# Run type checking
uv run mypy src/
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GITHUB_TOKEN` | GitHub PAT for API access | Yes |
| `GITHUB_ORG` | GitHub organization name | Yes (Sentinel) |
| `GITHUB_REPO` | GitHub repository name | Yes (Sentinel) |
| `WEBHOOK_SECRET` | GitHub webhook secret | Yes (Notifier) |
| `SENTINEL_BOT_LOGIN` | Bot account login for locking | Optional |

## Documentation

- [Repository Summary](.ai-repository-summary.md) - Detailed project overview
- [Architecture](plan_docs/architecture.md) - System architecture documentation
- [Tech Stack](plan_docs/tech-stack.md) - Technology stack details

## License

MIT License
