from tkinter import filedialog


class FileHandler:
    def open_file_name(self):
        filename = filedialog.askopenfilename(title='open')
        return filename

    def rgb_to_gray(self):
        pass
