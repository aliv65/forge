"""Cost estimation for Forge mock LLM usage."""

from analytics.token_usage import TokenUsage


class CostCalculator:
    """Calculates estimated LLM request cost from token usage."""

    def __init__(
        self,
        prompt_price: float = 0.000003,
        completion_price: float = 0.000006
    ) -> None:
        self.prompt_price = prompt_price
        self.completion_price = completion_price

    def calculate(
        self,
        usage: TokenUsage
    ) -> float:
        """Returns estimated request cost in US dollars."""

        return round(
            usage.prompt_tokens * self.prompt_price
            + usage.completion_tokens * self.completion_price,
            6
        )
