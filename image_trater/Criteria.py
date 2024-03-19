class ICriteria:
    def get(self):
        """
        Abstract method to get the the criteria elem.
        """
        pass

    def sumall(self):
        """
        Abstract method to get the brightness of the object.
        """
        pass

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
        t = list(zip(*self.brightness))
        print(t)
        return [sum(t) for t in list(zip(*self.brightness))]  # RGB brightness avg

    def div(self, x):
        r = [((l / r) for l, r in zip(t, x)) for t in self.brightness]
        return r
