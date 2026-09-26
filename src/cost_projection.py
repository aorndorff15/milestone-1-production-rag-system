from src.cost_tracker import CostTracker


def project_costs(requests_per_day: int, avg_input_tokens: int, 
                  avg_output_tokens: int, model: str = "gpt-4.1-mini",
                  cache_hit_rate: float = 0.0) -> dict:
    """Project costs at scale."""
    tracker_temp = CostTracker()
    
    # Effective requests (accounting for cache)
    effective_requests = requests_per_day * (1 - cache_hit_rate)
    
    # Cost per request
    cost_per_request = tracker_temp.calculate_cost(model, avg_input_tokens, avg_output_tokens)
    
    daily_cost = effective_requests * cost_per_request
    monthly_cost = daily_cost * 30
    yearly_cost = daily_cost * 365
    
    return {
        "model": model,
        "requests_per_day": requests_per_day,
        "effective_requests": effective_requests,
        "cache_hit_rate": cache_hit_rate,
        "cost_per_request": cost_per_request,
        "daily_cost": daily_cost,
        "monthly_cost": monthly_cost,
        "yearly_cost": yearly_cost
    }
