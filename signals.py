from runtime.values import Value


class StopSignal(Exception):
    pass


class SkipSignal(Exception):
    pass


class ReturnSignal(Exception):
    def __init__(self, value: Value):
        self.value = value
