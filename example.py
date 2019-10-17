import multitasking

if __name__ == "__main__":
    messages = multitasking.Queue()
    blah = multitasking.Queue()

    def hello():
        while True:
            blah.put("Hello world!")
            multitasking.sleep(0.25, sync=True)

    async def ping():
        try:
            messages.put("Ping pong!")
            await multitasking.sleep(1.0)
        except multitasking.CancelledError:
            messages.put("Task cancelled!")

    async def main(manager):
        proc = manager.add_process(hello)
        i = 0

        while True:
            try:
                print(messages.get_nowait())
            except:
                pass

            try:
                print(blah.get_nowait())
            except:
                pass

            if i == 5:
                manager.delete_process(proc)
                blah.put("Processed cancelled!")

            task = manager.add_task(ping)

            await multitasking.sleep(0.5)

            manager.delete_task(task)

            i += 1

    try:
        tm = multitasking.Manager()
        tm.add_task(main, tm)
        tm.start()
    except KeyboardInterrupt:
        pass
