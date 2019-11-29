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
  - [Known Issues](#known-issues)
    - [Recursive spawning](#recursive-spawning)
    - [Pipe/Queue corruption](#pipequeue-corruption)

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

Instances of the `Manager` class provide an asynchronous event loop to the program. Currently pytasking **only supports 1 asynchronous event loop** at any given time.

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
      # Normally you catch the cancel event and do something with it, but in this case, use it to break the loop and allow the task to close the task.
      break
    except:
      raise
```

Tasks will start immediately and you may add a task anytime.

#### `delete_task(t_id)`

Given a task id, you can call to delete a task. This method calls the `cancel()` method of the coroutine, it will give the coroutine the chance to cleanup and even deny the request if caught and handled in the `pytasking.CancelledError`.

#### `get_task(t_id)`

If you want to retrieve the underlying coroutine, you can use this method and provide the task id to get it.

#### `get_tasks()`

This will return all the task ids as a list, you can use this method in conjunction with `get_task(t_id)`.

#### `add_proc(proc, *args, **kwargs)`

#### `delete_proc(p_id)`

#### `get_proc(p_id)`

If you want to retrieve the underlying process, you can use this method and provide the process id to get it.

#### `get_procs()`

This will return all the process ids as a list, you can use this method in conjunction with `get_process(p_id)`.

#### `start()`

## Known Issues

### Recursive spawning

There maybe situations where you cannot spawn a task in a task, process in a process, task in a process, or a process in a task. I'll need to investigate further.

### Pipe/Queue corruption

If you decide to delete a process be wary, if the process was in the middle of accessing a Queue or Pipe, that Queue or Pipe will be liable to corruption and will not be usable again.