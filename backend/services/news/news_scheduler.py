"""
News Scheduler Service for SahyogSetu
Orchestrates automated incremental background collection of government announcements.
Provides controls for start, stop, immediate single-run execution, and status inspection.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from .news_collector import NewsCollector

logger = logging.getLogger("sahyogsetu.news.scheduler")

class NewsScheduler:
    """Manages periodic execution of news collectors in the background."""

    def __init__(self, interval_seconds: int = 3600):
        self.interval_seconds = interval_seconds
        self.is_running = False
        self._task: Optional[asyncio.Task] = None
        self.collector = NewsCollector()
        self.last_run: Optional[str] = None
        self.next_run: Optional[str] = None
        self.total_runs: int = 0
        self.last_result: Optional[Dict[str, Any]] = None
        self.last_error: Optional[str] = None

    def start(self):
        """Starts background periodic execution."""
        if self.is_running:
            logger.info("News scheduler already running.")
            return

        self.is_running = True
        self._task = asyncio.create_task(self._periodic_loop())
        logger.info("News scheduler started with %d-second interval.", self.interval_seconds)

    def stop(self):
        """Stops background periodic execution."""
        if not self.is_running:
            return

        self.is_running = False
        if self._task and not self._task.done():
            self._task.cancel()
        logger.info("News scheduler stopped.")

    async def run_once(self) -> Dict[str, Any]:
        """Executes a single immediate news collection run."""
        now = datetime.now()
        self.last_run = now.isoformat()
        try:
            logger.info("Starting scheduled news collection run #%d", self.total_runs + 1)
            result = await self.collector.collect_and_process_all()
            self.total_runs += 1
            self.last_result = result
            self.last_error = None
            if self.is_running:
                self.next_run = (now + timedelta(seconds=self.interval_seconds)).isoformat()
            return result
        except Exception as e:
            self.last_error = str(e)
            logger.error("News scheduler run failed: %s", e)
            return {"error": str(e), "timestamp": self.last_run}

    async def _periodic_loop(self):
        """Internal asynchronous loop running collection at specified interval."""
        while self.is_running:
            try:
                await self.run_once()
                await asyncio.sleep(self.interval_seconds)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.last_error = str(e)
                logger.error("Periodic loop exception: %s", e)
                await asyncio.sleep(60)

    def get_status(self) -> Dict[str, Any]:
        """Returns operational metrics and schedule state."""
        return {
            "is_running": self.is_running,
            "interval_seconds": self.interval_seconds,
            "total_runs": self.total_runs,
            "last_run": self.last_run,
            "next_run": self.next_run,
            "last_result": self.last_result,
            "last_error": self.last_error,
        }

# Global singleton scheduler instance
news_scheduler = NewsScheduler()

if __name__ == "__main__":
    async def main():
        print("=== SahyogSetu News Scheduler Single Run ===")
        scheduler = NewsScheduler()
        res = await scheduler.run_once()
        print(f"Collection result: {res}")
        print(f"Scheduler status: {scheduler.get_status()}")

    asyncio.run(main())
