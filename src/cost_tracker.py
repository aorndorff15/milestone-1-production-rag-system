# Pricing per 1K tokens (as of 2024 - verify current prices!)
PRICING = {
    "gpt-4.1-mini": {"input": 0.0004, "output": 0.0016, "provider": "OpenAI/Azure"},
    "gpt-4o": {"input": 0.0025, "output": 0.01, "provider": "OpenAI/Azure"},
    "gpt-4o-mini": {"input": 0.00015, "output": 0.0006, "provider": "OpenAI/Azure"},
    "gpt-4-turbo": {"input": 0.01, "output": 0.03, "provider": "OpenAI/Azure"},
    "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015, "provider": "OpenAI/Azure"},
    "gpt-5.6-sol": {"input": 0.004, "output": 0.02, "provider": "OpenAI/Azure"},
    "text-embedding-ada-002": {"input": 0.0001, "output": 0, "provider": "OpenAI/Azure"}
}

def estimate_cost(prompt_tokens: int, completion_tokens: int, model: str = "gpt-4.1-mini") -> float:
    """Estimate cost in USD for a given number of tokens."""
    if model not in PRICING:
        print(f"Warning: Unknown model {model}, using gpt-4.1-mini pricing")
        model = "gpt-4.1-mini"
    
    prices = PRICING[model]
    input_cost = (prompt_tokens / 1000) * prices["input"]
    output_cost = (completion_tokens / 1000) * prices["output"]
    return input_cost + output_cost

class CostTracker:
    """Track costs across multiple API calls."""
    
    def __init__(self):
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_cost = 0.0
        self.call_count = 0
    
    def track(self, response, model: str = "gpt-4.1-mini"):
        """Track a response's token usage and cost."""
        self.total_prompt_tokens += response.usage.prompt_tokens
        self.total_completion_tokens += response.usage.completion_tokens
        
        cost = estimate_cost(
            response.usage.prompt_tokens,
            response.usage.completion_tokens,
            model
        )
        
        self.total_cost += cost
        self.call_count += 1
        return cost
    
    def summary(self):
        """Print a summary of usage."""
        print(f"\n{'='*50}")
        print("COST SUMMARY")
        print(f"{'='*50}")
        print(f"Total API calls: {self.call_count}")
        print(f"Total prompt tokens: {self.total_prompt_tokens:,}")
        print(f"Total completion tokens: {self.total_completion_tokens:,}")
        print(f"Total tokens: {self.total_prompt_tokens + self.total_completion_tokens:,}")
        print(f"Total cost: ${self.total_cost:.6f}")
        
        if self.call_count > 0:
            print(f"Average cost per call: ${self.total_cost/self.call_count:.6f}")
