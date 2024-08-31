# From Python
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkScrollableFrame, CTk as ctk
from threading import Thread, Event
from PIL import Image, ImageTk
from tkinter import Label
import sys
import cv2
import time
import random

# Belong to the project
from app_coms.defaults import *
from app_coms.tech_sp import *

class AppMain:
    
    def __init__(self, title:str="", icon:str=""):
        self.title = title
        self.icon = icon
        self.app = ctk()
        self.app.overrideredirect(True)

        TechSupports.transparent_color(self.app, AppColors.TRANSPARENT)

        self.reg_thread = RecognitionThread()

        self.setup()

    def setup(self):
        title_bar = AppTitleBar(self, self.title)
        title_bar.pack(fill="x")

        window = AppWindow(self)
        window.pack(fill="x")

        self.app.geometry(f"{AppSpec.WIDTH}x{AppSpec.HEIGHT}")

    def run(self):
        self.reg_thread.start()
        self.app.mainloop()

    def stop(self):
        self.reg_thread.stop()
        self.app.destroy()
        sys.exit()


class AppTitleBar(CTkFrame):

    def __init__(self, root, title: str="", icon: str=""):
        self.root = root
        self.app = root.app
        self.title = title
        self.icon = icon

        super().__init__(self.app, corner_radius=10, background_corner_colors=(AppColors.TRANSPARENT, AppColors.TRANSPARENT, AppColors.WHITE, AppColors.WHITE), width=AppSpec.WIDTH, height=AppSpec.TITLE_BAR, fg_color=AppColors.WHITE)

        self.bar_setup()

    def bar_setup(self):
        # Window Movement
        self.bind("<ButtonPress-1>", self.bar_old_xy)
        self.bind("<B1-Motion>", self.bar_move)
        self.bind("<Map>",self.window_expand)

        # Window Icon
        icon_image = Image.open(AppSpec.LOGO)
        icon_image = icon_image.resize((AppSpec.ICON_SIZE, AppSpec.ICON_SIZE))
        icon = ImageTk.PhotoImage(icon_image)
        self.icon_label = Label(self, image=icon, bg=AppColors.WHITE, width=AppSpec.ICON_SIZE, height=AppSpec.ICON_SIZE)
        self.icon_label.image = icon  # Keep a reference to prevent garbage collection
        self.icon_label.pack(side="left", padx=10)
        self.icon_label.bind("<ButtonPress-1>", self.bar_old_xy)
        self.icon_label.bind("<B1-Motion>", self.bar_move)

        # Window Title
        self.bar_title = Label(self, text=self.title, font=(AppSpec.FONT, 15, "bold") ,
                               foreground=AppColors.BLACK, background=AppColors.WHITE)
        self.bar_title.bind("<ButtonPress-1>", self.bar_old_xy)
        self.bar_title.bind("<B1-Motion>", self.bar_move)
        self.bar_title.pack(side="left")

        # Close button
        self.bar_exit_btn = CTkButton(self, text="",cursor="hand2",
                  corner_radius=200, fg_color=AppColors.RED, hover_color=AppColors.GRAY, width=AppSpec.ICON_SIZE, height=AppSpec.ICON_SIZE, command=self.bar_close)
        self.bar_exit_btn.pack(side="right", padx=(5, 10), pady=5)

        # Minimize button
        self.bar_minimize_btn = CTkButton(self, text="",cursor="hand2",
                  corner_radius=200, fg_color=AppColors.YELLOW, hover_color=AppColors.GRAY, width=AppSpec.ICON_SIZE, height=AppSpec.ICON_SIZE)
        self.bar_minimize_btn.pack(side="right", pady=5)
        self.bar_minimize_btn.bind("<Button-1>", self.bar_minimize)

    def bar_move(self, event):
        self.y = event.y_root - self.oldy
        self.x = event.x_root - self.oldx
        self.app.geometry(f"+{self.x}+{self.y}")

    def bar_old_xy(self, event):
        self.oldx = event.x
        self.oldy = event.y

    def bar_close(self):
        self.root.stop()

    def window_expand(self,e):
        self.app.update_idletasks()
        self.app.overrideredirect(True)
        self.app.state('normal')

    def bar_minimize(self, event):
        self.app.update_idletasks()
        self.app.overrideredirect(False)
        self.app.state('iconic')

class AppWindow(CTkFrame):

    def __init__(self, root):
        self.root = root
        self.app = root.app
        # self.app.overrideredirect(True)

        # WIDTH = 830 
        super().__init__(self.app, corner_radius=10, background_corner_colors=(AppColors.GRAY, AppColors.GRAY, AppColors.TRANSPARENT, AppColors.TRANSPARENT), width=AppSpec.WIDTH, height=AppSpec.HEIGHT-AppSpec.TITLE_BAR, fg_color=AppColors.GRAY)

        self.sub_frame = []

        self.setup()

    def setup(self):
        self.intro_frame = IntroFrame(self.root, self)
        self.intro_frame.pack(padx=5, pady=5)
        self.intro_frame.place(x=5, y=5)
        self.sub_frame.append(self.intro_frame)

        self.cam_frame = CameraFrame(self.root, self)
        self.cam_frame.pack(padx=5, pady=5)
        self.cam_frame.place(x=AppSpec.WIDTH+5, y=5)
        self.sub_frame.append(self.cam_frame)

        self.sum_frame = SummaryFrame(self.root, self)
        self.sum_frame.pack(padx=5, pady=5)
        self.sum_frame.place(x=AppSpec.WIDTH+5, y=5)
        self.sub_frame.append(self.sum_frame)

    def switch_frame(self, index):
        for i in range(len(self.sub_frame)):
            if i==index:
                self.sub_frame[i].open()
            else:
                self.sub_frame[i].close()


class AppFrame(CTkLabel):

    def __init__(self, root, root_frame):
        self.root = root
        self.root_frame = root_frame
        super().__init__(self.root_frame, width=AppSpec.WIDTH-10, height=AppSpec.HEIGHT-AppSpec.TITLE_BAR-10, corner_radius=5, fg_color=AppColors.BACKGROUND0)

        self.setup()

    def setup(self):
        pass

    def start(self):
        pass

    def open(self):
        self.place(x=5, y=5)

    def close(self):
        self.place(x=AppSpec.WIDTH+5, y=5)

class TableItem:

    def __init__(self, name:str, time:str, table:CTkFrame):
        self.frame = CTkFrame(table)
        self.frame.pack(fill="x")

        self.name_label = CTkLabel(self.frame, text=name, height=30, width=200, fg_color=AppColors.BLACK, font=(AppSpec.FONT, 15), text_color=AppColors.WHITE, corner_radius=2)
        self.name_label.pack(side="left", padx=(0,2))
        self.name_label.place(x=5, y=5)

        self.time_label = CTkLabel(self.frame, text=time, height=30, width=300, fg_color=AppColors.BLACK, font=(AppSpec.FONT, 15), text_color=AppColors.WHITE, corner_radius=2)
        self.time_label.pack(side="left", padx=(0,5))
        self.time_label.place(x=210, y=5)

        self.detail_btn = CTkButton(self.frame, text = "<3",height=30, width=40, fg_color=AppColors.GREEN, font=(AppSpec.FONT, 15, "bold"), text_color=AppColors.BLACK, corner_radius=5)
        self.detail_btn.pack(side="right", padx=5, pady=5)


class IntroFrame(AppFrame):

    def __init__(self, root, root_frame):
        super().__init__(root, root_frame)
        
    def setup(self):
        # Start Button
        self.start_btn = CTkButton(self, text="Start",cursor="hand2", text_color=AppColors.BLACK,
                  corner_radius=200, fg_color=AppColors.RED,
                  hover_color=AppColors.GRAY, 
                  width=100, height=40, 
                  font=(AppSpec.FONT, 20, "bold"),
                  command=lambda: self.root_frame.switch_frame(1))
        self.start_btn.place(x=365, y=345)

class CameraFrame(AppFrame):

    def __init__(self, root, root_frame):
        super().__init__(root, root_frame)

    def setup(self):
        self.camera_running = False

        self.cap = cv2.VideoCapture(AppSpec.CAMERA_INDEX)

        self.camera_label = CTkLabel(self, text="",width=560, height=315, corner_radius=10, fg_color=AppColors.BLACK, bg_color=AppColors.BACKGROUND0)
        self.camera_label.place(x=135, y=15)

        self.camera_btn = CTkButton(self, text="Open", text_color=AppColors.BLACK, font=(AppSpec.FONT, 20, "bold"), 
                                    command=self.camera, width=100, height=35,
                                    corner_radius=200, fg_color=AppColors.GREEN,
                                    hover_color=AppColors.GRAY)
        self.camera_btn.place(x=165, y=345)

        self.exit_btn = CTkButton(self, text="Exit", text_color=AppColors.BLACK, font=(AppSpec.FONT, 20, "bold"), 
                                    command=lambda: self.root_frame.switch_frame(0), width=100, height=35,
                                    corner_radius=200, fg_color=AppColors.RED,
                                    hover_color=AppColors.GRAY)
        self.exit_btn.place(x=565, y=345)

        self.results_btn = CTkButton(self, text="Results", text_color=AppColors.BLACK, font=(AppSpec.FONT, 20, "bold"), 
                                   command=lambda: self.root_frame.switch_frame(2), width=100, height=35,
                                    corner_radius=200, fg_color=AppColors.YELLOW,
                                    hover_color=AppColors.GRAY)
        self.results_btn.place(x=365, y=345)

    def open_camera(self):
        if not self.camera_running:
            self.camera_label.configure(corner_radius=0, fg_color=AppColors.BACKGROUND0)
            self.cap = cv2.VideoCapture(1)
            self.camera_running = True
            self.update_frame()

    def update_frame(self):
        if self.camera_running:
            self.camera_btn.configure(text="Close")

            _, frame = self.cap.read()
            frame = cv2.flip(frame, 1)

            opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            captured_image = Image.fromarray(opencv_image)

            TechSupports.display_to_label(self.camera_label, captured_image)

            self.camera_label.after(10, self.update_frame)

    def close_camera(self):
        if self.camera_running:
            self.camera_btn.configure(text="Open")

            self.camera_running = False
            self.cap.release()  # Release the camera

            # Display a black blank frame
            TechSupports.blank_label(self.camera_label)

    def camera(self):
        if not self.camera_running:
            self.open_camera()
        else:
            self.close_camera()

    def close(self):
        self.close_camera()
        super().close()

class SummaryFrame(AppFrame):

    def __init__(self, root, root_frame):
        super().__init__(root, root_frame)
        self.items = []
        root.reg_thread.frame = self

    def setup(self):
        self.header_frame = CTkFrame(self, height=40, width=580, fg_color="#1A1A1A")
        self.header_frame.place(x=130, y=50)

        self.name_label = CTkLabel(self.header_frame, text = "Mã điểm danh",height=30, width=200, fg_color=AppColors.BACKGROUND0, font=(AppSpec.FONT, 15, "bold"), text_color=AppColors.WHITE, corner_radius=2)
        self.name_label.place(x=5, y=5)

        self.time_label = CTkLabel(self.header_frame, text="Thời gian điểm danh",height=30, width=300, fg_color=AppColors.BACKGROUND0, font=(AppSpec.FONT, 15, "bold"), text_color=AppColors.WHITE, corner_radius=2)
        self.time_label.place(x=210, y=5)

        self.table_frame = CTkScrollableFrame(self, width=560, height=200, fg_color=AppColors.BACKGROUNDTABLE)
        self.table_frame.place(x=124, y=90)

        self.exit_btn = CTkButton(self, text="Exit", text_color=AppColors.BLACK, font=(AppSpec.FONT, 20, "bold"), 
                                    command=lambda: self.root_frame.switch_frame(1), width=100, height=35,
                                    corner_radius=200, fg_color=AppColors.RED,
                                    hover_color=AppColors.GRAY)
        self.exit_btn.place(x=565, y=345)

    def open(self):
        super().open()
        self.show_table()

    def show_table(self):
        self.clear_table()
        for item in self.items:
            TableItem(item['maso'], item['thoigian'], self.table_frame)

    def clear_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

    def close(self):
        self.clear_table()
        super().close()


class RecognitionThread(Thread):

    def __init__(self):
        super().__init__()
        self.frame = None
    
    def run(self):
        # Get API here
        while self.frame:
            try:
                num_rand = random.randint(1,100)
                reg_list = []
                num_rand = random.randint(1,3)
                for i in range(num_rand):
                    reg_list.append({"maso":f"Ma so {i}",
                                    "thoigian": f"Thoi gian {i}"})
                
                self.frame.items = reg_list
                self.frame.show_table()
            except tk.TclError:
                pass
            time.sleep(5)
            

    def showing(self):
        print("Summary")

    def stop(self):
        self.frame = None
        self.join()
