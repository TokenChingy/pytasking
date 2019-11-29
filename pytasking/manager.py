import asyncio
import multiprocessing


class Manager:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            import uvloop
            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        except:
            pass

        self.__started = False
        self.__tasks = {}
        self.__procs = {}
        self.loop = asyncio.get_event_loop()

    async def __tasks__(self):
        await asyncio.gather(*self.__tasks.values())

    def __procs__(self):
        for p in self.__procs.values():
            p.start()

        self.__started = True

    def add_task(self, task, *args, **kwargs):
        t = asyncio.ensure_future(task(*args, **kwargs))
        t_id = hash(t)
        self.__tasks[t_id] = t
        return t_id

    def delete_task(self, t_id):
        self.__tasks[t_id].cancel()
        del self.__tasks[t_id]

    def get_task(self, t_id):
        return self.__tasks[t_id]

    def get_tasks(self):
        return [*self.__tasks.keys()]

    def add_proc(self, proc, *args, **kwargs):
        p = multiprocessing.Process(
            target=proc,
            args=args,
            kwargs=kwargs
        )
        p.daemon = True
        p_id = hash(p)
        self.__procs[p_id] = p

        if self.__started:
            p.start()

        return p_id

    def delete_proc(self, p_id):
        self.__procs[p_id].terminate()
        self.__procs[p_id].join()

    def get_proc(self, p_id):
        return self.__procs[p_id]

    def get_procs(self):
        return [*self.__procs.keys()]

    def start(self):
        self.__procs__()
        self.loop.run_until_complete(asyncio.ensure_future(self.__tasks__()))
        self.loop.close()
