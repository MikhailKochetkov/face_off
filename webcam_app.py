from tkinter import *
import time
import PIL.Image
import PIL.ImageTk
import cv2


class WebCamApplication(Toplevel):
    def __init__(self, video_source=0):
        super().__init__()
        self.title("use webcam")
        self.geometry("650x530")
        self.resizable(True, True)
        self.video_source = video_source
        self.create_webcam_widgets()

    def create_webcam_widgets(self):
        self.vid = VideoCapture(self.video_source)
        self.canvas = Canvas(self, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()
        self.btn_snapshot = Button(self, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=CENTER, expand=True)
        self.delay = 10
        self.update()

    def snapshot(self):
        ret, frame = self.vid.get_frame()
        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
        ret, frame = self.vid.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
        self.after(self.delay, self.update)


class VideoCapture:
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("unable to open video source", video_source)
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self, ret=None):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return ret, None
        else:
            return ret, None

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

