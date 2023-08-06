from functools import wraps

from ..session_persist import SessionConfig

def session_call(user: SessionConfig):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with user:
                return func(*args, **kwargs)
        
        return wrapper
    
    return decorator