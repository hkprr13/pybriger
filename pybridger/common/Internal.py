#-------------------------------------------------------------------------------
import warnings
#-------------------------------------------------------------------------------
def internal(func):
    """内部専用API用デコレーター"""
    def wrapper(*args, **kwargs):
        warnings.warn(
            f"{func.__name__} is internal API and should not be used outside this library.",
            UserWarning
        )
        return func(*args, **kwargs)
    wrapper.__is_internal_api__ = True
    return wrapper
#-------------------------------------------------------------------------------