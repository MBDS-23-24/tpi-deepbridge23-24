from Slice import Slice
import os

class Main:

    def __init__(self):
        pass

    def run(self, src, dest):
        _slice = Slice()
        p = 0
        q = 1
        pixels_on_curve = _slice.get_pixels_on_curve(p, q, src)
        print(pixels_on_curve)
    
if __name__ == "__main__":
    main = Main()
    print(os.getcwd())
    main.run(src="p1.png", dest="result.jpg")
