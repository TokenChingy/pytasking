# Pytasking

A simple library for Python 3.5+ that provides an easy interface for multitasking.

## Table of Contents

- [Pytasking](#pytasking)
  - [Table of Contents](#table-of-contents)
  - [Dependencies](#dependencies)
  - [Usage](#usage)

## Dependencies

- Python 3.5+

*There are no external module dependencies outside of the standard library however, if you'd like to take advantage of `uvloop`, you can install that and the `pytasking` library will use it automatically (Only available on Linux/MacOS).*

## Usage

- Include the directory `pytasking` in your project root directory.
- If on Linux/MacOS; run `python -m pip install -r requirements.txt`.

A basic python example:

```python
#!/usr/bin/env python

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
    except pytasking.CancelledError:
      print("Pang!")
      break


async def main(task_manager):
  hellos = 0
  hello_queue = pytasking.Queue()
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
    except pytasking.CancelledError:
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
```

There maybe situations where you cannot spawn a task in a task, process in a process, task in a process, or a process in a task – these will be the edge cases.

If you decide to delete a process be wary, if the process was in the middle of accessing a Queue or Pipe, that Queue or Pipe will be liable to corruption and will not be usable again.