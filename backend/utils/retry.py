import time
from functools import wraps

def retry_on_rate_limit(max_retries=2, base_delay=60):
    """Retry a function once or twice if it hits a 429, waiting Google's suggested delay."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    is_last_attempt = attempt == max_retries
                    if "429" in str(e) and not is_last_attempt:
                        print(f"Rate limited. Waiting {base_delay}s (retry {attempt + 1}/{max_retries})...")
                        time.sleep(base_delay)
                        continue
                    raise
        return wrapper
    return decorator