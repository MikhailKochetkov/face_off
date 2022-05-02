from tkinter import filedialog


class FileHandler:
    def open_image_name(self):
        imagename = filedialog.askopenfilename(title='open image')
        return imagename

    def open_model_name(self):
        pass

    def rgb_to_gray(self):
        pass
