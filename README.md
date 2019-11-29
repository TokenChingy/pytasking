# Pytasking

A simple library for Python 3.5+ that provides an easy interface for multitasking.

## Table of Contents

- [Pytasking](#pytasking)
  - [Table of Contents](#table-of-contents)
  - [Dependencies](#dependencies)
  - [Installation](#installation)
    - [Source](#source)
    - [PyPi](#pypi)
  - [Usage](#usage)
  - [API](#api)
    - [`class pytasking.Manager()`](#class-pytaskingmanager)
      - [`add_task(task, *args, **kwargs)`](#addtasktask-args-kwargs)
      - [`delete_task(t_id)`](#deletetasktid)
      - [`get_task(t_id)`](#gettasktid)
      - [`get_tasks()`](#gettasks)
      - [`add_proc(proc, *args, **kwargs)`](#addprocproc-args-kwargs)
      - [`delete_proc(p_id)`](#deleteprocpid)
      - [`get_proc(p_id)`](#getprocpid)
      - [`get_procs()`](#getprocs)
      - [`start()`](#start)

## Dependencies

- Python 3.5+

*There are no external module dependencies outside of the standard library however, if you'd like to take advantage of `uvloop`, you can install that and the `pytasking` library will use it automatically (Only available on Linux/MacOS).*

## Installation

### Source

- Include the directory `pytasking` in your project root directory.
- If on Linux/MacOS; run `python -m pip install -r requirements.txt`.

### PyPi

- Run `pip install pytasking`.

## Usage

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

## API

### `class pytasking.Manager()`

Instances of the `Manager` class provide an asynchronous event loop to the program. Currently pytasking only **supports 1 asynchronous event loop** at any given time.

Asynchronous tasks and parallel processes are spawned and managed by the `Manager` instance.

#### `add_task(task, *args, **kwargs)`

Create an asynchronous task from a function definition. Pass arguments and keyword arguments as you would normally. This function returns an id from the has of the task. You can use the id to retrieve and delete the task. Make sure you define your function with the following template:

```python
async def asynchronous_task_definition(): # Define any arguments or keyword arguments as you normally would.
  # Do whatever you need to do here as you normally would.

  # If you want this task to run indefinitely, do this:
  while True:
    try:
      # Do something forever.
    except pytasking.CancelledError: # This one is important.
      break
    except:
      raise
```

#### `delete_task(t_id)`

#### `get_task(t_id)`

#### `get_tasks()`

#### `add_proc(proc, *args, **kwargs)`

#### `delete_proc(p_id)`

#### `get_proc(p_id)`

#### `get_procs()`

#### `start()`

There maybe situations where you cannot spawn a task in a task, process in a process, task in a process, or a process in a task – these will be the edge cases.

If you decide to delete a process be wary, if the process was in the middle of accessing a Queue or Pipe, that Queue or Pipe will be liable to corruption and will not be usable again.