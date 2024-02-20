import time

from fastapi import Request


async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = round(time.time() - start_time, 4)
    response.headers['X-Process-Time'] = str(process_time)
    return response
