# System Architecture - workflow-orchestration-queue

## Overview

workflow-orchestration-queue is an **Autonomous AI Orchestration System** that transforms GitHub Issues into execution orders fulfilled by specialized AI agents without human intervention. The system follows a "Self-Bootstrapping" philosophy where it can build and evolve itself using its own orchestration capabilities.

## Core Components

### 1. Work Event Notifier ("The Ear")

The system's primary gateway for external stimuli and asynchronous triggers.

**Technology:** Python 3.12, FastAPI, UV, Pydantic

**Responsibilities:**
- **Secure Webhook Ingestion** - Hardened endpoint for GitHub events (issues, issue_comment, pull_request)
- **Cryptographic Verification** - HMAC SHA256 validation against WEBHOOK_SECRET to prevent prompt injection attacks
- **Intelligent Event Triage** - Parses payloads into unified WorkItem objects with structured manifests
- **Queue Initialization** - Applies `agent:queued` label to trigger Sentinel processing

### 2. Work Queue ("The Logic State")

Distributed state management using GitHub's native features.

**Philosophy:** "Markdown as a Database" - leveraging GitHub for audit logs, versioning, and UI.

**State Machine (Label Logic):**
| Label | State | Description |
|-------|-------|-------------|
| `agent:queued` | Awaiting | Task validated, awaiting Sentinel pickup |
| `agent:in-progress` | Active | Sentinel claimed task, execution underway |
| `agent:reconciling` | Recovery | Stale task detected, awaiting re-assignment |
| `agent:success` | Complete | Workflow finished successfully |
| `agent:error` | Failed | Technical failure, logs posted to issue |

**Concurrency Control:** Uses GitHub "Assignees" as distributed lock with assign-then-verify pattern.

### 3. Sentinel Orchestrator ("The Brain")

The persistent supervisor managing Worker lifecycle and task dispatch.

**Technology:** Python Async, PowerShell Core, Docker CLI

**Responsibilities:**
- **Polling Discovery** - Scans for `agent:queued` issues every 60 seconds with jittered exponential backoff on rate limits
- **Auth Synchronization** - Ensures valid tokens via gh-auth.ps1
- **Shell-Bridge Protocol** - Manages Worker via devcontainer-opencode.sh (up, start, prompt)
- **Workflow Mapping** - Translates issue types to specific prompt strings
- **Heartbeat Telemetry** - Posts status comments every 5 minutes during long-running tasks
- **Graceful Shutdown** - Handles SIGTERM/SIGINT to prevent orphaned tasks

### 4. Opencode Worker ("The Hands")

The agentic execution environment that performs actual work.

**Technology:** opencode CLI, LLM (GLM-5, Claude)

**Capabilities:**
- **Contextual Awareness** - Accesses project structure with vector-indexed views
- **Instructional Logic** - Reads and executes workflow modules from /local_ai_instruction_modules/
- **Verification** - Runs test suites before PR submission to ensure zero-regression

## Data Flow (Happy Path)

```
User Issue → Notifier (webhook) → Label: agent:queued
         ↓
Sentinel (poll) → Assign & Label: in-progress
         ↓
devcontainer-opencode.sh up → start → prompt
         ↓
Worker executes → Posts results
         ↓
Sentinel → Label: agent:success → PR Created
```

## Security Architecture

- **Network Isolation** - Workers in dedicated Docker network
- **Credential Scoping** - Tokens passed via temporary env vars
- **Credential Scrubbing** - All logs sanitized before GitHub visibility
- **Resource Constraints** - CPU/RAM limits prevent rogue agent DoS

## Key Architectural Decisions

1. **ADR-07: Shell-Bridge Execution** - Orchestrator uses devcontainer-opencode.sh exclusively for container management
2. **ADR-08: Polling-First Resiliency** - Polling as primary discovery; webhooks as optimization
3. **ADR-09: Provider-Agnostic Interface** - ITaskQueue abstraction enables future provider swapping

## Self-Bootstrapping Lifecycle

1. **Bootstrap** - Manual clone of template repository
2. **Seed** - Add plan docs to repo
3. **Init** - Run devcontainer-opencode.sh up
4. **Orchestrate** - Agent configures its own environment
5. **Autonomous** - Sentinel service runs, AI manages all future development
