from abc import ABC, abstractmethod


class ICriteria(ABC):
    @abstractmethod
    def get(self):
        """
        Abstract method to get the the criteria elem.
        """
        pass

    @abstractmethod
    def sumall(self):
        """
        Abstract method to get the brightness of the object.
        """
        pass

    @abstractmethod
    def div(self, x):
        """
        Abstract method to get the brightness of the object.
        """
        pass


class CriteriaBrightness(ICriteria):
    def __init__(self, brightness):
        self.brightness = brightness

    def get(self):
        return self.brightness

    def sumall(self):
        return [sum(t) for t in list(zip(*self.brightness))]  # RGB brightness avg

    def div(self, x):
        return [[left / right if right != 0 else 0 for left, right in zip(t, x)] for t in self.brightness]
