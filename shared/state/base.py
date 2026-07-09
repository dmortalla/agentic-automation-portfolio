"""Shared workflow state models."""

from enum import StrEnum

from pydantic import BaseModel, Field


class WorkflowStatus(StrEnum):
    """Supported workflow execution statuses."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class BaseWorkflowState(BaseModel):
    """Base workflow state shared by all agentic automation projects.

    Attributes:
        status: Current workflow execution status.
        errors: List of recoverable or terminal workflow errors.
    """

    status: WorkflowStatus = Field(default=WorkflowStatus.PENDING)
    errors: list[str] = Field(default_factory=list)

    def add_error(self, message: str) -> None:
        """Add an error message and mark the workflow as failed.

        Args:
            message: Error message to record.

        Raises:
            ValueError: If the message is blank.
        """
        cleaned_message = message.strip()

        if not cleaned_message:
            raise ValueError("Error message must not be blank.")

        self.errors.append(cleaned_message)
        self.status = WorkflowStatus.FAILED
