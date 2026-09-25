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
