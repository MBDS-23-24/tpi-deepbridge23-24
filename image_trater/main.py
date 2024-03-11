import Slice

class Main:

    def __init__(self):
        pass

    def run(self, src, dest):
        _slice = Slice()
        # _slice.generate_image(src, dest)
        p = 1
        q = 0
        pixels_on_curve = _slice.get_pixels_on_curve(p, q, src)
        print(pixels_on_curve)
    
if __name__ == "__main__":
    main = Main()
    main.run(src="p1.png", dest="image.jpg")
