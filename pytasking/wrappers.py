import asyncio
import multiprocessing

CancelledError = asyncio.CancelledError

Pipe = multiprocessing.Pipe
Queue = multiprocessing.Queue

Barrier = multiprocessing.Barrier
Condition = multiprocessing.Condition
Event = multiprocessing.Event
Lock = multiprocessing.Lock
RLock = multiprocessing.RLock
Semaphore = multiprocessing.Semaphore
Timer = multiprocessing.Timer
