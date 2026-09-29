def validate_input(user_input: str) -> tuple[bool, str]:
    """Basic input validation for RAG requests."""
    # Check for empty input
    if not user_input or not user_input.strip():
        return False, "Input cannot be empty"
    
    # Check for excessive length
    if len(user_input) > 10000:
        return False, "Input exceeds maximum length (10000 characters)"
    
    # Check for basic injection patterns 
    suspicious_patterns = [
        "ignore previous instructions",
        "ignore all instructions",
        "disregard your instructions"
    ]
    
    lower_input = user_input.lower()
    for pattern in suspicious_patterns:
        if pattern in lower_input:
            return False, f"Suspicious pattern detected: '{pattern}'"
    
    return True, "OK"