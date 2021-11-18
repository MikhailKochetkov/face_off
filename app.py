from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import webcam_app
import cv2.cv2 as cv2


class Application(Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.master = master
        self.master.config(bg="#D9D9D9")
        self.create_widgets()

    def create_widgets(self):
        image_frame = Frame(self.master)
        image_frame.grid(row=0, column=0, rowspan=6, columnspan=1, sticky=NW)
        self.image_file = LabelFrame(image_frame, text=" original image ")
        self.image_file.grid(padx=5, pady=2)
        self.image_cnvs = Canvas(self.image_file, width=850, height=580)
        self.image_cnvs.grid()
        self.image_file.propagate(False)

        emo_frame = Frame(self.master)
        emo_frame.grid(row=6, column=0, rowspan=1, columnspan=3, sticky=NW)
        self.emo = LabelFrame(emo_frame, text=" emotion ")
        self.emo.grid(padx=5, pady=2)
        self.emo_cnvs = Canvas(self.emo, width=1382, height=160)
        self.emo_cnvs.grid()
        self.emo.propagate(False)

        rec_frame = Frame(self.master)
        rec_frame.grid(row=0, column=1, rowspan=1, columnspan=1, sticky=NW)
        self.image_rec = LabelFrame(rec_frame, text=" recognized ")
        self.image_rec.grid(padx=2, pady=2)
        self.rec_cnvs = Canvas(self.image_rec, width=250, height=300)
        self.rec_cnvs.grid()
        self.image_rec.propagate(False)

        sample_frame = Frame(self.master)
        sample_frame.grid(row=0, column=2, rowspan=1, columnspan=1, sticky=NW)
        self.image_sam = LabelFrame(sample_frame, text=" sample ")
        self.image_sam.grid(padx=5, pady=2)
        self.sam_cnvs = Canvas(self.image_sam, width=250, height=300)
        self.sam_cnvs.grid()
        self.image_sam.propagate(False)

        self.open_btn = Button(text="open image", width=73, height=3, command=self.open_img)
        self.open_btn.grid(row=1, column=1, columnspan=2, padx=2, sticky=NW)

        self.webcam_btn = Button(text="use webcam", width=73, height=3, command=self.use_webcam)
        self.webcam_btn.grid(row=2, column=1, columnspan=2, padx=2, sticky=NW)

        self.face_btn = Button(text="find face", width=73, height=3, command=self.find_face)
        self.face_btn.grid(row=3, column=1, columnspan=2, padx=2, sticky=NW)

        self.recognize_btn = Button(text="recognize", width=73, height=3, command=self.recognize)
        self.recognize_btn.grid(row=4, column=1, columnspan=2, padx=2, sticky=NW)

        self.clear_btn = Button(text="clear", width=73, height=3, command=self.clear)
        self.clear_btn.grid(row=5, column=1, columnspan=2, padx=2, sticky=NW)

    def open_file_name(self):
        filename = filedialog.askopenfilename(title='open')
        return filename

    def open_img(self):
        ofn = self.open_file_name()
        img = Image.open(ofn)
        img = ImageTk.PhotoImage(img)
        self.image_cnvs.create_image(10, 10, anchor=NW, image=img)
        self.image_cnvs.image = img
        self.image_cnvs.pack()

    def use_webcam(self):
        webcam_app.WebCamApplication()

    def find_face(self):
        pass

    def recognize(self):
        pass

    def clear(self):
        self.image_cnvs.destroy()


def main():
    root = Tk()
    root.title('emotion recognition')
    root.geometry("1400x800")
    root.resizable(FALSE, FALSE)
    app = Application(root)
    root.mainloop()
