import functools
from starlette.responses import JSONResponse


def request_exception_handler(function):
    @functools.wraps(function)
    async def wrapper(*args, **kwargs):
        try:
            return await function(*args, **kwargs)
        except Exception as ex:
            message = "Error while processing request: {}".format(ex)
            return JSONResponse(
                status_code=400,
                content={"message": message},
            )

    return wrapper
