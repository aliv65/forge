"""LLM token usage model."""

from dataclasses import dataclass


@dataclass(slots=True)
class TokenUsage:
    """Stores token usage for a single LLM request."""

    prompt_tokens: int = 0

    completion_tokens: int = 0

    total_tokens: int = 0

    def __post_init__(self) -> None:
        if self.prompt_tokens < 0 or self.completion_tokens < 0:
            raise ValueError("Token counts cannot be negative.")

        calculated_total = (
            self.prompt_tokens
            + self.completion_tokens
        )

        if self.total_tokens not in (0, calculated_total):
            raise ValueError(
                "Total tokens must equal prompt and completion tokens."
            )

        self.total_tokens = calculated_total
