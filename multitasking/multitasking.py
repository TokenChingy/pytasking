import asyncio
import logging
import multiprocessing


class Manager:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            import uvloop

            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        except:
            logging.info(
                "Python3 module `uvloop` not found, defaulting to standard asyncio event loop policy."
            )

        self.__started = False
        self.__loop = asyncio.get_event_loop()
        self.__tasks = {}
        self.__processes = {}

    async def __tasks__(self):
        await asyncio.gather(*self.__tasks.values())

    def add_task(self, task, *args, **kwargs):
        t = asyncio.ensure_future(task(*args))
        t_id = hash(t)
        self.__tasks[t_id] = t
        return t_id

    def delete_task(self, t_id):
        self.__tasks[t_id].cancel()
        del self.__tasks[t_id]

    def add_process(self, proc, *args, **kwargs):
        p = multiprocessing.Process(
            target=proc,
            args=args,
            kwargs=kwargs
        )
        p.daemon = True
        p_id = hash(p)
        self.__processes[p_id] = p

        if self.__started:
            p.start()

        return p_id

    def delete_process(self, p_id):
        self.__processes[p_id].terminate()
        self.__processes[p_id].join()

    def start(self):
        logging.info("Multitasking manager started...")

        for p in self.__processes.values():
            p.start()

        self.__started = True
        self.__loop.run_until_complete(asyncio.ensure_future(self.__tasks__()))
        self.__loop.close()
