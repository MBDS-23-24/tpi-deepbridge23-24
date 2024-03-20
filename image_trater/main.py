import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import ttk

from Slice import Slice

path = os.getcwd()
dst_root = f"{path}/examples/tests/line2D/results"

def run(posa, posb, src, dest):
    _slice = Slice()
    return _slice.generate_image(posa, posb, src, dest, debug=True)

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.startX = tk.StringVar()
        self.startY = tk.StringVar()
        self.endX = tk.StringVar()
        self.endY = tk.StringVar()
        self.input_image_path = None
        self.input_image_label = None
        self.imagewidth = tk.IntVar()
        self.imageheight = tk.IntVar()
        self.sliders = {}
        self.slider_vars = []
        self.generate_image_path = None
        self.output_image_label = None

        self.master = master
        self.pack()
        self.create_widgets()
        self.master.title("Application cut images")
        self.master.geometry("600x700")  # Set the dimensions of the window

    def create_widgets(self):
        # Label and Entry for displaying input image
        self.input_label = tk.Label(self, text="Input Image")
        self.input_label.pack()
        self.canvas = tk.Canvas(self)
        self.canvas.pack()

        # Button to open input image
        self.open_button = tk.Button(self, text="Open ref image", command=self.open_image)
        self.open_button.pack(pady=5)

    def initialize_sliders(self):
        # Sliders for x0, y0, x1, y1
        self.slider_vars = [("x0", self.startX, self.imagewidth), ("y0", self.startY, self.imageheight),
                            ("x1", self.endX, self.imagewidth), ("y1", self.endY, self.imageheight)]
        for label_text, var, v in self.slider_vars:
            label = tk.Label(self, text=label_text)
            label.pack()

            slider_frame = tk.Frame(self)
            slider_frame.pack()

            slider = ttk.Scale(slider_frame, from_=0, to=v.get(), orient=tk.HORIZONTAL, variable=var,
                               command=self.update_line)
            slider.set(0)
            slider.pack(side="left")
            self.sliders[label_text] = slider

            value_label = tk.Label(slider_frame, textvariable=var)
            value_label.pack(side="left")

        self.init_generate()

    def init_generate(self):
        # Call the function to get the generated image path
        self.generate_button = tk.Button(self, text="Generate images cut", command=self.generate_image)
        self.generate_button.pack(pady=5)

        self.output_label = tk.Label(self, text="Output Image")
        self.output_label.pack()
        self.output_image_label = tk.Label(self)
        self.output_image_label.pack()

    def open_image(self):
        self.input_image_path = filedialog.askopenfilename()
        if self.input_image_path:
            input_image = Image.open(self.input_image_path)

            input_photo = ImageTk.PhotoImage(input_image)
            input_photo = input_photo._PhotoImage__photo.zoom(35, 35)  # Resize image for display

            self.imagewidth.set(input_photo.width())
            self.imageheight.set(input_photo.height())

            self.canvas.config(width=input_photo.width(), height=input_photo.height())
            self.input_image_label = self.canvas.create_image(0, 0, anchor=tk.NW, image=input_photo)
            self.canvas.image = input_photo

            if len(self.slider_vars) == 0:
                # Initialize sliders
                self.initialize_sliders()

            self.update_sliders()  # Update the sliders' maximum values after image upload

    def update_sliders(self):
        # Update the maximum values of sliders
        for lt, _, v in self.slider_vars:
            self.sliders[lt].config(to=v.get())

    def generate_image(self):
        src, filename = os.path.split(self.input_image_path)
        print("Source:", src)
        print("Filename:", filename)

        dst = dst_root + '/' + filename
        pos1 = (int(float(self.startX.get())/35), int(float(self.startY.get())/35))
        pos2 = (int(float(self.endX.get())/35), int(float(self.endY.get())/35))
        print(pos1, pos2)
        run(pos1, pos2, src + '/', dst)
        self.generate_image_path = dst
        print("done")



        if self.generate_image_path:
            output_image = Image.open(self.generate_image_path)

            output_photo = ImageTk.PhotoImage(output_image)
            output_photo = output_photo._PhotoImage__photo.zoom(35, 35)  # Resize image for display

            self.output_image_label.config(image=output_photo)
            self.output_image_label.image = output_photo
        else:
            print("nothing to do with")


    def update_line(self, event=None):
        try:
            self.startX.set(int(float(self.startX.get())))
            self.startY.set(int(float(self.startY.get())))
            self.endX.set(int(float(self.endX.get())))
            self.endY.set(int(float(self.endY.get())))

            x0 = self.startX.get()
            y0 = self.startY.get()
            x1 = self.endX.get()
            y1 = self.endY.get()

            # Delete existing line
            self.canvas.delete("line")

            # Draw new line
            self.canvas.create_line(x0, y0, x1, y1, fill="#00FF00", width=6, tags="line")
        except ValueError as err:
            print(err)
            self.canvas.create_line(0, 0, 0, 0, fill="#00FF00", width=6, tags="line")



root = tk.Tk()
app = Application(master=root)
app.mainloop()
