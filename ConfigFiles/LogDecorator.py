from ConfigFiles.Logger_config import logger
#
# def log_activity(action_name):
#     """
#     Decorator to log the success or failure of actions.
#     :param action_name: The name of the action being logged (e.g., 'Add Book').
#     """
#
#     def decorator(func):
#         def wrapper(*args, **kwargs):
#             try:
#                 # Attempt to execute the function
#                 result = func(*args, **kwargs)
#                 # Log success
#                 logger.info(f"{action_name} successfully")
#                 return result
#             except Exception as e:
#                 # Log failure
#                 logger.error(f"{action_name} fail")
#                 raise  # Re-raise the exception
#
#         return wrapper
#
#     return decorator

from ConfigFiles.Logger_config import logger

def log_activity(action_name):
    """
    Decorator to log the success or failure of actions.
    :param action_name: The name of the action being logged (e.g., 'Add Book').
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                # Execute the function
                result = func(*args, **kwargs)
                logger.info(f"{action_name} successfully")
                return result

            except Exception as e:
                # Log unhandled exceptions
                logger.error(f"{action_name} fail")
                raise # Re-raise the exception

        return wrapper
    return decorator


def search_log_activity(action_name):
    """
    Decorator to log the success or failure of search actions.
    :param action_name: The name of the action being logged (e.g., 'Search Book by Title').
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                # Extract query details from args/kwargs
                query = kwargs.get('query', args[1] if args else 'Unknown Query')

                # Execute the wrapped function
                result = func(*args, **kwargs)

                # Log success with specific format
                logger.info(f"Search book '{query}' by {action_name} completed successfully")
                return result

            except Exception as e:
                # Log failure with specific format
                logger.error(f"Search book '{query}' by {action_name} failed")
                return None  # Return None or handle the exception gracefully

        return wrapper
    return decorator