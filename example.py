#!/usr/bin/env python3

import pytasking
import time


def hello(hello_queue):
    while True:
        hello_queue.put_nowait("Hello World!")
        pytasking.sleep(1.5, sync=True)


async def ping():
    while True:
        try:
            print("Ping!")
            await pytasking.sleep(1.0)
            print("Pong!")
        except pytasking.asyncio.CancelledError:
            print("Pang!")
            break


async def main(task_manager):
    hellos = 0
    hello_queue = pytasking.multiprocessing.Queue()
    hello_proc = task_manager.add_proc(hello, hello_queue)

    while True:
        try:
            if hellos == 5:
                task_manager.delete_proc(hello_proc)

            if hello_queue.qsize() > 0:
                try:
                    print(hello_queue.get_nowait())
                    hellos += 1
                except:
                    pass

            ping_task = task_manager.add_task(ping)
            await pytasking.sleep(0.5)
            task_manager.delete_task(ping_task)
        except pytasking.asyncio.CancelledError:
            break


if __name__ == "__main__":
    task_manager = pytasking.Manager()
    task_manager.add_task(main, task_manager)

    try:
        task_manager.start()
    except KeyboardInterrupt:
        pass
    except:
        raise
