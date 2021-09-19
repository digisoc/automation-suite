""" Module Imports """
# import traceback


def debug(func):
    """try/except decorator which replies with exception traceback information"""

    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            # exception = traceback.format_exc() # would not advise exposing
            ctx = args[0]
            if ctx:
                await ctx.reply(e)
            raise

    return wrapper
