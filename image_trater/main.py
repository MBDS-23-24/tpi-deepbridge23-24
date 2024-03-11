import Slice
import Donati

class Main:

    def __init__(self):
        pass

    def run(self, src, dest):
        _slice = Slice()
        _slice.generate_image(src, dest)
    
if __name__ == "__main__":
    main = Main()
    main.run()
