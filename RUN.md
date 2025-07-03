# Running the Components

## Setup

Install dependencies:

```bash
uv sync
```

## Run the Server

Start the HTTP server:

```bash
uv run python -m uvicorn app.server:app --reload
```

The server will be available at http://localhost:8000

### Server Endpoints

- `GET /status` - Get current status
- `POST /start` - Start the status transition (none → in-progress → pass/fail)
- `POST /reset` - Reset status to "none" (for testing)

## Run the Polling Script

In another terminal, run the polling script:

```bash
uv run python app/watch.py
```

Options:

- `--server-url URL` - Server URL to poll (default: http://localhost:8000)
- `--interval SECONDS` - Polling interval (default: 10)

## Test Integration

Run the integration test:

```bash
uv run python test_integration.py
```

## GitHub Actions

The workflow is configured in `.github/workflows/claude.yml` and will:

1. Trigger on pull requests to main branch
2. Run the polling script against an external server
3. Exit with appropriate code based on server status

To use with an external server, set the `EXTERNAL_SERVER_URL` secret in your
repository settings.