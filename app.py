from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
import PIL
from PIL import ImageTk, Image
import webcam_app
import cv2.cv2 as cv2
import time
import os
import numpy as np
import csv
from tensorflow.keras.models import load_model
import pandas as pd
from constants import *
import image_handler as ih


class Application(Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.master = master
        self.master.config(bg="#D9D9D9")
        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self.master, width=1400, height=800)
        notebook.pack()

        main_frame = ttk.Frame(notebook)
        # neural_net_frame = ttk.Frame(notebook)
        notebook.add(main_frame, text='main screen')
        # notebook.add(neural_net_frame, text='neural network')

        self.image_file = ttk.LabelFrame(main_frame, text=" original image ")
        self.image_file.grid(row=0, column=0, rowspan=6, columnspan=1, padx=5, pady=2, sticky=NW)
        self.image_cnvs = Canvas(self.image_file, width=850, height=580)
        self.image_cnvs.grid()
        self.image_file.propagate(False)

        self.emo = ttk.LabelFrame(main_frame, text=" emotion ")
        self.emo.grid(row=6, column=0, rowspan=1, columnspan=3, padx=5, pady=2, sticky=NW)
        self.emo_cnvs = Canvas(self.emo, width=1382, height=160)
        self.emo_cnvs.grid()
        self.emo.propagate(False)

        self.image_rec = ttk.LabelFrame(main_frame, text=" recognized ")
        self.image_rec.grid(row=0, column=1, rowspan=1, columnspan=1, padx=2, pady=2, sticky=NW)
        self.rec_cnvs = Canvas(self.image_rec, width=250, height=300)
        self.rec_cnvs.grid()
        self.image_rec.propagate(False)

        self.image_sam = ttk.LabelFrame(main_frame, text=" sample ")
        self.image_sam.grid(row=0, column=2, rowspan=1, columnspan=1, padx=5, pady=2, sticky=NW)
        self.sam_cnvs = Canvas(self.image_sam, width=250, height=300)
        self.sam_cnvs.grid()
        self.image_sam.propagate(False)

        self.open_btn = Button(main_frame, text="open image", width=73, height=3, command=self.open_img)
        self.open_btn.grid(row=1, column=1, columnspan=2, padx=2, sticky=NW)

        self.webcam_btn = Button(main_frame, text="use webcam", width=73, height=3, command=self.use_webcam)
        self.webcam_btn.grid(row=2, column=1, columnspan=2, padx=2, sticky=NW)

        self.face_btn = Button(main_frame, text="find face", width=73, height=3, command=self.find_face)
        self.face_btn.grid(row=3, column=1, columnspan=2, padx=2, sticky=NW)

        self.recognize_btn = Button(main_frame, text="recognize", width=73, height=3, command=self.recognize)
        self.recognize_btn.grid(row=4, column=1, columnspan=2, padx=2, sticky=NW)

        self.clear_btn = Button(main_frame, text="clear", width=73, height=3, command=self.clear)
        self.clear_btn.grid(row=5, column=1, columnspan=2, padx=2, sticky=NW)

    def open_img(self):
        try:
            self.ofn = ih.ImageHandler.open_file_name(self)
            img = Image.open(self.ofn)
            img = ImageTk.PhotoImage(img)
            self.image_cnvs.create_image(10, 10, anchor=NW, image=img)
            self.image_cnvs.image = img
            self.image_cnvs.pack()
        except PIL.UnidentifiedImageError:
            messagebox.showinfo("Info", "The selected file is not an image")

    def use_webcam(self):
        webcam_app.WebCamApplication()

    def find_face(self):
        try:
            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            face_rec = cv2.imread(self.ofn)
            gray = cv2.cvtColor(face_rec, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            if not np.any(faces):
                messagebox.showinfo("Info", "Face not found")
            else:
                for (x, y, w, h) in faces:
                    cv2.rectangle(face_rec, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.imwrite("image-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", face_rec)
                file = max(os.listdir(), key=os.path.getctime)
                self.image_cnvs.delete("all")
                file_img = Image.open(file)
                file_img = ImageTk.PhotoImage(file_img)
                self.image_cnvs.create_image(10, 10, anchor=NW, image=file_img)
                self.image_cnvs.image = file_img
                self.image_cnvs.pack()
                crop = face_rec[y:y + h, x:x + w]
                cv2.imwrite("crop-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", crop)
                crop_file = max(os.listdir(), key=os.path.getctime)
                crop_img = Image.open(crop_file)
                crop_img = crop_img.resize((230, 230), Image.ANTIALIAS)
                crop_img = ImageTk.PhotoImage(crop_img)
                self.rec_cnvs.create_image(10, 10, anchor=NW, image=crop_img)
                self.rec_cnvs.image = crop_img
                self.rec_cnvs.pack()
        except Exception:
            messagebox.showinfo("Info", "File not selected")

    def recognize(self):
        crp_file = max(os.listdir(), key=os.path.getctime)
        crp_img = Image.open(crp_file)
        resize_img = crp_img.resize((48, 48), Image.ANTIALIAS)
        resize_img_gray = resize_img.convert('L')
        value = np.asarray(resize_img_gray.getdata(), dtype=np.int32).reshape(
            (resize_img_gray.size[1], resize_img_gray.size[0]))
        value = value.flatten()
        with open("resize-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".csv", 'a') as f:
            writer = csv.writer(f, delimiter=' ')
            writer.writerow(value)
            f.close()
        img_csv = pd.read_csv(f.name)
        sample_faces = []
        for pixel_sequence in img_csv:
            face = [int(pixel) for pixel in pixel_sequence.split()]
            face = np.asarray(face).reshape(IMG_SIZE, IMG_SIZE)
            face = face / 255.0
            sample_faces.append(face.astype('float32'))
        sample_faces = np.asarray(sample_faces)
        sample_faces = np.expand_dims(sample_faces, -1)
        model = load_model('fer_model.h5')
        predictions = model.predict(sample_faces, verbose=0)
        txt = "This image most likely belongs to {} with a {:.2f} percent confidence".format(
            EMOTIONS[np.argmax(predictions)], round(100 * np.max(predictions), 2))
        self.emo_cnvs.create_text(650, 80, text=txt, justify=CENTER, font="Verdana 24")
        self.emo_cnvs.pack()
        sam_img = Image.open("./samples/" + EMOTIONS[np.argmax(predictions)] + ".jpg")
        sam_img = sam_img.resize((230, 230), Image.ANTIALIAS)
        sam_img = ImageTk.PhotoImage(sam_img)
        self.sam_cnvs.create_image(10, 10, anchor=NW, image=sam_img)
        self.sam_cnvs.image = sam_img
        self.sam_cnvs.pack()

    def clear(self):
        self.image_cnvs.delete("all")
        self.rec_cnvs.delete("all")
        self.sam_cnvs.delete("all")
        self.emo_cnvs.delete("all")

    def on_closing(self):
        for i in os.listdir():
            if i.endswith(".jpg") or i.endswith(".csv"):
                os.remove(os.path.join(os.getcwd(), i))


def main():
    root = Tk()
    root.title('emotion recognition')
    root.geometry("1430x840")
    root.resizable(FALSE, FALSE)
    app = Application(root)
    root.mainloop()
    app.on_closing()
