from abc import abstractmethod


class Test:
    def __init__(self, name: str, conf: dict) -> None:
        self._name = name.split('.')[-1:][0]  # remove tester.test.

    @abstractmethod
    def run(self) -> bool:
        pass

    @property
    def name(self) -> str:
        return self._name
