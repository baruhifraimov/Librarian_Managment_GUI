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

                # Check if the function handled an exception (by returning a specific flag)
                if isinstance(result, dict) or not result:
                    logger.error(f"{action_name} failed (handled exception internally)")
                else:
                    logger.info(f"{action_name} successfully completed")

                return result

            except Exception as e:
                # Log unhandled exceptions
                logger.error(f"{action_name} failed with unhandled exception: {str(e)}")
                raise  # Re-raise the exception

        return wrapper
    return decorator