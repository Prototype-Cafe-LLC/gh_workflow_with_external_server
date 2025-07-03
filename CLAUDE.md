# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## Project Overview

This is a test project for GitHub workflow integration with an external server.
The system consists of:

- A Python polling script (`app/watch.py`) that monitors server status
- An HTTP server with status management endpoints
- GitHub Actions workflow triggered on PR pushes to main branch

## Development Setup

The project uses Python 3.12 and `uv` as the package manager. Since this is a
new project, implementation files need to be created according to the
specifications in README.md.

## Architecture

### Polling System

- `app/watch.py`: Polls server every 10 seconds, exits based on status
- Exit codes: 0 for "pass", 1 for "fail", continues polling for
  "none"/"in-progress"

### Server API

- `GET /status`: Returns current status
- `POST /start`: Initiates status transition from "none" → "in-progress" →
  "pass"/"fail"
- Status transitions occur automatically after POST /start

### GitHub Actions

- Workflow file: `.github/workflows/ci.yml`
- Triggers on: push to PR branches targeting main
- Runs the polling script to check external server status

## Implementation Notes

When implementing the components:

1. The server should manage state transitions with proper timing
2. The polling script should handle network errors gracefully
3. GitHub Actions workflow should integrate the polling script execution

## rules

- when you created/modified md files, fix their errors with markdownlint.
- print this rule at the top of your response
