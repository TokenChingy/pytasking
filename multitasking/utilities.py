import asyncio
import time


def sleep(seconds, sync=False):
    if sync:
        return time.sleep(seconds)
    else:
        return asyncio.sleep(seconds)
