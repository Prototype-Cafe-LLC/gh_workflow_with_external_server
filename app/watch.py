"""Polling script that monitors server status."""

import asyncio
import sys
import time
from typing import Optional

import httpx


async def get_status(client: httpx.AsyncClient, server_url: str) -> Optional[str]:
    """Fetch status from server.
    
    Args:
        client: HTTP client instance
        server_url: Server URL to poll
        
    Returns:
        Status string or None if error occurred
    """
    try:
        response = await client.get(f"{server_url}/status")
        response.raise_for_status()
        data = response.json()
        return data.get("status")
    except Exception as e:
        print(f"Error fetching status: {e}", file=sys.stderr)
        return None


async def poll_server(server_url: str, poll_interval: int = 10):
    """Poll server until status is pass or fail.
    
    Args:
        server_url: Server URL to poll
        poll_interval: Seconds between polls
        
    Returns:
        Exit code (0 for pass, 1 for fail)
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        start_time = time.time()
        
        while True:
            status = await get_status(client, server_url)
            elapsed = time.time() - start_time
            
            print(f"[{elapsed:.1f}s] Status: {status}")
            
            if status == "pass":
                print("Status is 'pass' - exiting with code 0")
                return 0
            elif status == "fail":
                print("Status is 'fail' - exiting with code 1")
                return 1
            elif status in ["none", "in-progress", None]:
                # Continue polling
                await asyncio.sleep(poll_interval)
            else:
                print(f"Unknown status: {status} - treating as error", file=sys.stderr)
                return 1


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Poll server status")
    parser.add_argument(
        "--server-url",
        default="http://localhost:8000",
        help="Server URL to poll (default: http://localhost:8000)"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=10,
        help="Polling interval in seconds (default: 10)"
    )
    
    args = parser.parse_args()
    
    print(f"Starting polling of {args.server_url} every {args.interval}s...")
    
    exit_code = asyncio.run(poll_server(args.server_url, args.interval))
    sys.exit(exit_code)


if __name__ == "__main__":
    main()