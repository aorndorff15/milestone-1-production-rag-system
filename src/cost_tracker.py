# Pricing per 1K tokens (as of 2024 - verify current prices!)
PRICING_DB = {
    # OpenAI / Azure OpenAI
    "gpt-4.1-mini": {"input": 0.0004, "output": 0.0016, "provider": "OpenAI/Azure"},
    "gpt-4o": {"input": 0.0025, "output": 0.01, "provider": "OpenAI/Azure"},
    "gpt-4o-mini": {"input": 0.00015, "output": 0.0006, "provider": "OpenAI/Azure"},
    "gpt-4-turbo": {"input": 0.01, "output": 0.03, "provider": "OpenAI/Azure"},
    "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015, "provider": "OpenAI/Azure"},
    "gpt-5.6-sol": {"input": 0.004, "output": 0.02, "provider": "OpenAI/Azure"},
    
    # Anthropic
    "claude-3-5-sonnet": {"input": 0.003, "output": 0.015, "provider": "Anthropic"},
    "claude-3-opus": {"input": 0.015, "output": 0.075, "provider": "Anthropic"},
    "claude-3-haiku": {"input": 0.00025, "output": 0.00125, "provider": "Anthropic"},
    
    # Google
    "gemini-1.5-pro": {"input": 0.00125, "output": 0.005, "provider": "Google"},
    "gemini-1.5-flash": {"input": 0.000075, "output": 0.0003, "provider": "Google"},
    
    # Embeddings
    "text-embedding-ada-002": {"input": 0.0001, "output": 0, "provider": "OpenAI/Azure"},
    "text-embedding-3-small": {"input": 0.00002, "output": 0, "provider": "OpenAI"},
}

@dataclass
class APICallRecord:
    """Record of a single API call."""
    timestamp: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost_usd: float
    latency_ms: float
    success: bool
    error: Optional[str] = None
    cache_hit: bool = False
    

class CostTracker:
    """Comprehensive cost tracking for LLM API calls."""
    
    def __init__(self, pricing_db: dict = None):
        self.pricing = pricing_db or PRICING_DB
        self.records: List[APICallRecord] = []
        
    def calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """Calculate cost for a given usage."""
        if model not in self.pricing:
            # Try to find a matching model
            model = "gpt-4.1-mini"  # Default fallback
        
        prices = self.pricing[model]
        input_cost = (prompt_tokens / 1000) * prices["input"]
        output_cost = (completion_tokens / 1000) * prices["output"]
        return input_cost + output_cost
    
    def record_call(self, response, model: str, latency_ms: float, 
                    cache_hit: bool = False, error: str = None):
        """Record an API call."""
        if error:
            record = APICallRecord(
                timestamp=datetime.now().isoformat(),
                model=model,
                prompt_tokens=0,
                completion_tokens=0,
                total_tokens=0,
                cost_usd=0,
                latency_ms=latency_ms,
                success=False,
                error=error,
                cache_hit=cache_hit
            )
        else:
            cost = self.calculate_cost(
                model,
                response.usage.prompt_tokens,
                response.usage.completion_tokens
            )
            record = APICallRecord(
                timestamp=datetime.now().isoformat(),
                model=model,
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
                cost_usd=cost,
                latency_ms=latency_ms,
                success=True,
                cache_hit=cache_hit
            )
        
        self.records.append(record)
        return record
    
    def get_summary(self) -> dict:
        """Get summary statistics."""
        if not self.records:
            return {"error": "No records"}
        
        df = pd.DataFrame([asdict(r) for r in self.records])
        
        return {
            "total_calls": len(self.records),
            "successful_calls": df["success"].sum(),
            "total_tokens": df["total_tokens"].sum(),
            "total_cost_usd": df["cost_usd"].sum(),
            "avg_latency_ms": df["latency_ms"].mean(),
            "cache_hit_rate": df["cache_hit"].mean() if "cache_hit" in df else 0,
            "cost_per_call": df["cost_usd"].mean(),
            "by_model": df.groupby("model")["cost_usd"].sum().to_dict()
        }
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convert records to DataFrame."""
        return pd.DataFrame([asdict(r) for r in self.records])
    
    def print_summary(self):
        """Print formatted summary."""
        s = self.get_summary()
        print("\n" + "="*50)
        print("COST TRACKING SUMMARY")
        print("="*50)
        print(f"Total API calls: {s['total_calls']}")
        print(f"Successful calls: {s['successful_calls']}")
        print(f"Total tokens: {s['total_tokens']:,}")
        print(f"Total cost: ${s['total_cost_usd']:.6f}")
        print(f"Average latency: {s['avg_latency_ms']:.0f}ms")
        print(f"Cache hit rate: {s['cache_hit_rate']:.1%}")
        print(f"Average cost per call: ${s['cost_per_call']:.6f}")
        print("\nCost by model:")
        for model, cost in s['by_model'].items():
            print(f"  {model}: ${cost:.6f}")
