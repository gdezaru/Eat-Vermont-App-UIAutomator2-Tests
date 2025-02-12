import functools
import time
import logging
from typing import Type, Union, Tuple

logger = logging.getLogger(__name__)

def retry(
    retries: int = 3,
    delay: float = 1,
    backoff: float = 2,
    exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]] = Exception
):
    """
    Retry decorator with exponential backoff for test methods.
    
    Args:
        retries: Number of times to retry the wrapped function
        delay: Initial delay between retries in seconds
        backoff: Multiplier applied to delay between retries
        exceptions: Exception(s) that trigger a retry
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retry_delay = delay
            last_exception = None
            
            for i in range(retries + 1):
                try:
                    if i > 0:
                        logger.info(f"Retry attempt {i} for {func.__name__}")
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if i == retries:  # Last attempt
                        logger.error(f"All {retries} retries failed for {func.__name__}")
                        raise  # Re-raise the last exception
                    
                    logger.warning(
                        f"Test {func.__name__} failed with {type(e).__name__}: {str(e)}. "
                        f"Retrying in {retry_delay} seconds..."
                    )
                    time.sleep(retry_delay)
                    retry_delay *= backoff  # Exponential backoff
            
            if last_exception:
                raise last_exception
        return wrapper
    return decorator
