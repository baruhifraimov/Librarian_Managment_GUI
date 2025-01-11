from ConfigFiles.Logger_config import logger

def log_activity(action_name):
    """
    Decorator to log the success or failure of actions.
    :param action_name: The name of the action being logged (e.g., 'Add Book').
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                # Attempt to execute the function
                result = func(*args, **kwargs)
                # Log success
                logger.info(f"{action_name} successfully")
                return result
            except Exception as e:
                # Log failure
                logger.error(f"{action_name} fail")
                raise  # Re-raise the exception

        return wrapper

    return decorator