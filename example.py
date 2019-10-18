#!/usr/bin/env python3

import multitasking
import time


def hello(hello_queue):
  while True:
    hello_queue.put_nowait("Hello World!")
    multitasking.sleep(1.5, sync=True)


async def ping():
  while True:
    try:
      print("Ping!")
      await multitasking.sleep(1.0)
      print("Pong!")
    except multitasking.CancelledError:
      print("Pang!")
      break


async def main(task_manager):
  hellos = 0
  hello_queue = multitasking.Queue()
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
      await multitasking.sleep(0.5)
      task_manager.delete_task(ping_task)
    except multitasking.CancelledError:
      break


if __name__ == "__main__":
  task_manager = multitasking.Manager()
  task_manager.add_task(main, task_manager)

  try:
    task_manager.start()
  except KeyboardInterrupt:
    pass
  except:
    raise