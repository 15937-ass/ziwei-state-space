"""
Ziwei Research Agent Runtime v0.1

Minimal orchestration skeleton.
This file defines execution order only.
Domain knowledge must stay in knowledge/ and sources/.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Task:
    task_id: str
    scope: str
    status: str = "pending"


class ResearchOrchestrator:
    def __init__(self):
        self.pipeline = [
            "A1_extract",
            "A4_validate",
            "A2_normalize",
            "A6_report"
        ]

    def run(self, task: Task):
        print(f"Start {task.task_id}: {task.scope}")
        for agent in self.pipeline:
            print(f"Executing {agent}")
        task.status = "completed"
        return task


if __name__ == "__main__":
    orchestrator = ResearchOrchestrator()
    orchestrator.run(Task(
        task_id="WP04-A",
        scope="Transformation operator extraction"
    ))
