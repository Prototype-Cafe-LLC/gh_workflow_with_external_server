"""HTTP server with state management for GitHub workflow testing."""

import asyncio
import random
from datetime import datetime
from enum import Enum
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Status(str, Enum):
    """Server status states."""
    
    NONE = "none"
    IN_PROGRESS = "in-progress"
    PASS = "pass"
    FAIL = "fail"


class StatusResponse(BaseModel):
    """Status API response model."""
    
    status: Status
    timestamp: datetime


class ServerState:
    """Manages server state transitions."""
    
    def __init__(self):
        self.status = Status.NONE
        self.transition_task: Optional[asyncio.Task] = None
        
    async def start_transition(self):
        """Initiate status transition from none to in-progress to pass/fail."""
        if self.status != Status.NONE:
            raise ValueError(f"Can only start from 'none' status, current: {self.status}")
            
        # Cancel any existing transition
        if self.transition_task and not self.transition_task.done():
            self.transition_task.cancel()
            
        # Immediately transition to in-progress
        self.status = Status.IN_PROGRESS
        self.transition_task = asyncio.create_task(self._run_transition())
        
    async def _run_transition(self):
        """Run the status transition sequence."""
        try:
            # Status is already in-progress from start_transition
            
            # Wait 5-15 seconds
            wait_time = random.uniform(5, 15)
            await asyncio.sleep(wait_time)
            
            # Randomly transition to pass or fail (80% pass, 20% fail)
            self.status = Status.PASS if random.random() > 0.2 else Status.FAIL
            
        except asyncio.CancelledError:
            # Reset to none if cancelled
            self.status = Status.NONE
            raise


# Global state instance
state = ServerState()


@app.get("/status", response_model=StatusResponse)
async def get_status():
    """Get current server status."""
    return StatusResponse(
        status=state.status,
        timestamp=datetime.now()
    )


@app.post("/start")
async def start_process():
    """Start the status transition process."""
    try:
        await state.start_transition()
        return {"message": "Process started", "status": state.status}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/reset")
async def reset_status():
    """Reset status to none (for testing purposes)."""
    if state.transition_task and not state.transition_task.done():
        state.transition_task.cancel()
    state.status = Status.NONE
    return {"message": "Status reset", "status": state.status}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)