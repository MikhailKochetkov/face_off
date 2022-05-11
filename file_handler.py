from tkinter import filedialog


class FileHandler:
    def open_image_name(self):
        imagename = filedialog.askopenfilename(title='open image', filetypes=(('JPEG', ('*.jpg', '*.jpeg')), ('All files', '*.*')))
        return imagename

    def open_model_name(self):
        modelname = filedialog.askopenfilename(title='open model', filetypes=(('Model files', '*.h5'), ('All files', '*.*')))
        return modelname

    def rgb_to_gray(self):
        pass

    def image_to_csv(self, image):
        pass

    def resize_image(self, image):
        pass
