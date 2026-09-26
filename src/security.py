def validate_input(user_input: str) -> tuple[bool, str]:
    """Basic input validation for LLM requests.
    
    Returns: (is_valid, message)
    """
    # Check for empty input
    if not user_input or not user_input.strip():
        return False, "Input cannot be empty"
    
    # Check for excessive length
    if len(user_input) > 10000:
        return False, "Input exceeds maximum length (10000 characters)"
    
    # Check for basic injection patterns (more in Module 9!)
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

def secure_chat(user_input: str, client, model: str) -> str:
    """Make an API call with basic security checks."""
    # Validate input
    is_valid, message = validate_input(user_input)
    if not is_valid:
        return f"Request blocked: {message}"
    
    # Make API call
    try:
        response = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=200
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"
