"""Work queue implementations."""

from orchestrator.queue.github_queue import ITaskQueue, GitHubQueue

__all__ = ["ITaskQueue", "GitHubQueue"]
