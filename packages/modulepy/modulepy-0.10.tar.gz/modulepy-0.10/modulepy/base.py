from multiprocessing import Queue, Process
from dataclasses import dataclass
from time import sleep


@dataclass
class ModuleVersion:
    major: int
    minor: int
    patch: int

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"


@dataclass
class ModuleInformation:
    name: str
    version: ModuleVersion

    def __str__(self):
        return f"{self.name} {self.version}"


@dataclass
class SharedData:
    origin: ModuleInformation
    data: dict


@dataclass
class IOQueue:
    in_queue: Queue
    out_queue: Queue

    def __init__(self):
        self.in_queue = Queue()
        self.out_queue = Queue()

    def input(self, data: SharedData):
        self.in_queue.put(data)

    def process_output(self, cb: callable):
        while not self.out_queue.empty():
            data = self.out_queue.get()
            cb(data)


class ModuleBase(Process):
    daemon = True

    do_run: bool = False
    information = ModuleInformation("ModuleBase", ModuleVersion(1, 0, 0))
    dependencies: list[ModuleInformation] = []

    queue: IOQueue = IOQueue()

    error: str = None

    def __init__(self):
        self.name = str(self.information)
        Process.__init__(self, name=self.name)

    def __call__(self, *args, **kwargs):
        return eval(f"{self.__class__.__name__}()")

    def on_start(self):
        self.do_run = True

    def on_stop(self):
        pass

    def work(self):
        sleep(0.1)

    def process_input_data(self, data: SharedData):
        pass

    def on_action_stop(self):
        self.stop()

    def on_action_start(self):
        self.run()

    def wait_until_stopped(self):
        while self.is_alive():
            sleep(0.1)

    def on_action_restart(self):
        self.stop()
        self.wait_until_stopped()
        self.run()

    def on_action_log(self, message: str):
        print(f"{self.name}: {message}")

    def process_system_data(self, data: SharedData):
        if data.origin.name == "ModuleManager":
            if data.data["action"] == "stop":
                self.on_action_stop()
            elif data.data["action"] == "start":
                self.on_action_start()
            elif data.data["action"] == "restart":
                self.on_action_restart()
            elif data.data["action"] == "log":
                self.on_action_log(data.data["message"])

    def loop(self):
        while self.do_run:
            self.queue.process_output(self.process_system_data)
            self.work()

    def _run(self):
        self.on_start()
        self.loop()
        self.on_stop()

    def run(self):
        print(f"{self.name}: Starting")
        self._run()

    def stop(self):
        self.do_run = False

    def enqueue(self, data: dict):
        self.queue.input(SharedData(self.information, data))
