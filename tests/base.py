from abc import ABC, abstractmethod


class TestMethod(ABC):

    @abstractmethod
    def test(self):
        pass