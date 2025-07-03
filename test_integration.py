"""Integration test for server and polling script."""

import asyncio
import subprocess
import time

import httpx


async def test_integration():
    """Test the integration between server and polling script."""
    # Start the server in a subprocess
    server_proc = subprocess.Popen(
        ["python", "-m", "uvicorn", "app.server:app", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    print("Waiting for server to start...")
    await asyncio.sleep(2)
    
    try:
        async with httpx.AsyncClient() as client:
            # Check initial status
            resp = await client.get("http://localhost:8000/status")
            print(f"Initial status: {resp.json()['status']}")
            
            # Start the process
            resp = await client.post("http://localhost:8000/start")
            print(f"Started process: {resp.json()}")
            
            # Run polling script in subprocess
            print("\nRunning polling script...")
            poll_proc = subprocess.run(
                ["python", "app/watch.py", "--interval", "2"],
                capture_output=True,
                text=True
            )
            
            print(f"Polling script output:\n{poll_proc.stdout}")
            print(f"Exit code: {poll_proc.returncode}")
            
    finally:
        # Clean up
        server_proc.terminate()
        server_proc.wait()
        print("\nServer stopped")


if __name__ == "__main__":
    asyncio.run(test_integration())