""" Module Imports """
import traceback


def debug(func):
    """try/except decorator which replies with exception traceback information"""

    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception:
            exception = traceback.format_exc()
            ctx = args[0]
            if ctx:
                await ctx.reply(exception)
            raise

    return wrapper
