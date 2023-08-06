from multiprocessing import Process

class emitter:
    funcs = []
    events = []
    _events = [
        "any_event"
        "on_ready"
    ]

    def __init__(self, funcs):
        self.funcs = funcs
        print(self.funcs)

    def send(self, name, args = []):
        for func in self.funcs:
            print(func.__name__)
            # if func.__name__ in self._events:
            func(args)

    class event:
        event = None
        def __init__(self, name="any_event", args=[]):
            self.evtname = name
            self.startThread()

        def awaitResponse(self, name="any_event"):
            while True:
                print(f"{self.evtname} is waiting")
                # wait for event
                emitter.send(name=name)
                print(f"{self.evtname} has been called")

        def startThread(self):
            Process(target=self.awaitResponse()).start()

    def prepare(self, funcs):
        self.funcs = funcs
        for _event in self._events:
            self.events.append(self.event(name=_event))




