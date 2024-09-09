# From Python
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkScrollableFrame, CTkToplevel, CTk as ctk
from threading import Thread
from PIL import Image, ImageTk
from tkinter import Label
from tkinter import PhotoImage
import sys
import cv2
from datetime import datetime

# Belong to the project
from app_coms.defaults import *
from app_coms.tech_sp import *
from app_coms.components import *

class AppMain:
    
    def __init__(self, title:str="", icon:str=""):
        self.title = title
        self.icon = icon
        self.app = ctk()
        self.app.overrideredirect(True)
        self.reg_list = []

        TechSupports.transparent_color(self.app, AppColors.TRANSPARENT)

        self.setup()

    def setup(self):

        self.title_bar = AppTitleBar(self, self.title)
        self.title_bar.pack(fill="x")

        self.window = AppWindow(self)
        self.window.pack(fill="x")

        # INTRO FRAME
        self.intro_frame = IntroFrame(self, self.window)
        self.intro_frame.place(x=5, y=5)

        # MAIN FRAME
        self.main_frame = MainFrame(self, self.window)
        self.main_frame.place(x=AppSpec.WIDTH+5, y=5)

        # MAIN SUB FRAME
        cam_frame = CameraFrame(self, self.main_frame)
        cam_frame.place(x=150, y=0)

        sum_frame = SummaryFrame(self, self.main_frame)
        sum_frame.place(x=AppSpec.WIDTH+5, y=5)

        # GEOMETRY APP
        self.app.geometry(f"{AppSpec.WIDTH}x{AppSpec.HEIGHT}")

    def show_noti(self, name):
        print("noti")
        # threading.Thread(target=TechSupports.play_sound).start()
        CustomMessageBox(self.app, title="Chào mừng!", name=name,icon=r'.\resources\cntt_logo100.png')

    def update_summary(self, name):
        self.main_frame.update_summary(self.reg_list[-1])
        self.show_noti(name)

    def run(self):
        self.app.mainloop()

    def stop(self):
        self.app.destroy()

class AppTitleBar(CTkFrame):

    def __init__(self, root, title: str="", icon: str=""):
        self.root = root
        self.app = root.app
        self.title = title
        self.icon = icon

        super().__init__(self.app, corner_radius=10, background_corner_colors=(AppColors.TRANSPARENT, AppColors.TRANSPARENT, AppColors.BACKGROUNDBAR, AppColors.BACKGROUNDBAR), width=AppSpec.WIDTH, height=AppSpec.TITLE_BAR, fg_color=AppColors.BACKGROUNDBAR)

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
        self.icon_label = Label(self, image=icon, bg=AppColors.BACKGROUNDBAR, width=AppSpec.ICON_SIZE, height=AppSpec.ICON_SIZE)
        self.icon_label.image = icon  # Keep a reference to prevent garbage collection
        self.icon_label.pack(side="left", padx=10)
        self.icon_label.bind("<ButtonPress-1>", self.bar_old_xy)
        self.icon_label.bind("<B1-Motion>", self.bar_move)

        # Window Title
        self.bar_title = Label(self, text=self.title, font=(AppSpec.FONT, 12, AppSpec.FONT_TITLE_W) ,
                               foreground=AppColors.BLACK, background=AppColors.BACKGROUNDBAR)
        self.bar_title.bind("<ButtonPress-1>", self.bar_old_xy)
        self.bar_title.bind("<B1-Motion>", self.bar_move)
        self.bar_title.pack(side="left")

        # Close button
        bar_exit_icon = Image.open('.\\resources\\bar_exit_icon.png')
        bar_exit_image = ImageTk.PhotoImage(image=bar_exit_icon)

        self.bar_exit_btn = CTkButton(self, text="",cursor="hand2",
                  corner_radius=200, fg_color=AppColors.RED, hover_color=AppColors.GRAY, 
                #   image=bar_exit_image,
                  width=AppSpec.ICON_SIZE, height=AppSpec.ICON_SIZE, command=self.bar_close)
        self.bar_exit_btn.pack(side="right", padx=(5, 10), pady=5)

        # Collapse button
        bar_collapse_icon = Image.open('.\\resources\\bar_collapse_icon.png')
        bar_collapse_image = ImageTk.PhotoImage(image=bar_collapse_icon)

        self.bar_collapse_btn = CTkButton(self, text="",cursor="hand2",
                  corner_radius=200, fg_color=AppColors.YELLOW, hover_color=AppColors.GRAY, 
                #   image=bar_collapse_image,
                  width=AppSpec.ICON_SIZE, height=AppSpec.ICON_SIZE)
        self.bar_collapse_btn.pack(side="right", pady=5)
        self.bar_collapse_btn.bind("<Button-1>", self.bar_collapse)

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

    def bar_collapse(self, event):
        self.app.update_idletasks()
        self.app.overrideredirect(False)
        self.app.state('iconic')

class AppWindow(CTkFrame):

    def __init__(self, root):
        self.root = root
        self.app = root.app

        # WIDTH = 830 
        super().__init__(self.app, corner_radius=10, background_corner_colors=(AppColors.GRAY, AppColors.GRAY, AppColors.TRANSPARENT, AppColors.TRANSPARENT), width=AppSpec.WIDTH, height=AppSpec.HEIGHT-AppSpec.TITLE_BAR, fg_color=AppColors.GRAY)

        self.sub_frame = []

        self.setup()

    def setup(self):
        pass

    def switch_frame(self, index):
        for i in range(len(self.sub_frame)):
            if i==index:
                self.sub_frame[i].open()
            else:
                self.sub_frame[i].close()

class AppFrame(CTkLabel):

    def __init__(self, root, root_frame, height=AppSpec.HEIGHT-AppSpec.TITLE_BAR-10, width=AppSpec.WIDTH-10, corner_radius=5):
        self.root = root
        self.root_frame = root_frame
        super().__init__(self.root_frame, width=width, height=height, corner_radius=corner_radius)
        self.setup()

    def setup(self):
        try:
            self.pack(padx=5, pady=5)
        except:
            pass
        self.root_frame.sub_frame.append(self)

    def start(self):
        pass

    def open(self):
        self.place(x=5, y=5)

    def close(self):
        self.place(x=AppSpec.WIDTH+5, y=5)

class TableItem:

    def __init__(self, item: dict, table:CTkFrame):
        self.frame = CTkFrame(table)
        self.frame.pack(fill="x")

        self.name_label = CTkLabel(self.frame, text=item['maso'], height=30, width=200, fg_color=AppColors.BLACK, font=(AppSpec.FONT, 15), text_color=AppColors.WHITE, corner_radius=2)
        self.name_label.pack(side="left", padx=(0,2))
        self.name_label.place(x=5, y=5)

        self.time_label = CTkLabel(self.frame, text=item['thoigian'], height=30, width=300, fg_color=AppColors.BLACK, font=(AppSpec.FONT, 15), text_color=AppColors.WHITE, corner_radius=2)
        self.time_label.pack(side="left", padx=(0,5))
        self.time_label.place(x=210, y=5)

        detail_icon = Image.open(".\\resources\\export_icon.png")
        detail_image = ImageTk.PhotoImage(image=detail_icon)

        self.detail_btn = CTkButton(self.frame, text = "",height=30, width=40, 
                                    fg_color=AppColors.LIGHT_BLUE, font=(AppSpec.FONT, 15, "bold"), 
                                    image=detail_image,
                                    text_color=AppColors.BLACK, corner_radius=5,
                                    command=lambda: TechSupports.open_folder(item['output']))
        self.detail_btn.pack(side="right", padx=5, pady=5)


class IntroFrame(AppFrame):

    def __init__(self, root, root_frame):
        super().__init__(root, root_frame)
        
    def setup(self):
        super().setup()
        self.configure(fg_color=AppColors.BACKGROUND0)

        # Start Button
        start_icon = Image.open('resources\\icons8-start-94.png')
        start_image = ImageTk.PhotoImage(image=start_icon)

        self.start_btn = CTkButton(self, text="",cursor="hand2", text_color=AppColors.BLACK,
                  corner_radius=15, fg_color=AppColors.BACKGROUND0,
                  image=start_image,
                  hover_color=AppColors.GRAY, 
                  width=300, height=100, 
                  font=(AppSpec.FONT, 20, "bold"),
                  command=lambda: self.root_frame.switch_frame(1))
                #   command=lambda: self.root.show_noti())
        self.start_btn.place(x=280, y=150)

class MainFrame(AppFrame):
    
    def __init__(self, root, root_frame):
        self.sub_frame = []
        self.frame_btn = []
        self.active_icon = ['.\\resources\\blue\\cam_icon_a.png','.\\resources\\blue\\table_icon_a.png']
        self.deactive_icon = ['.\\resources\\white\\cam_icon_d.png','.\\resources\\white\\table_icon_d.png']
        super().__init__(root, root_frame)
        
    def setup(self):
        super().setup()
        self.configure(fg_color=AppColors.BACKGROUND0)

        # # App Label
        hau_icon = Image.open(".\\resources\\hau_logo.png")
        hau_image = ImageTk.PhotoImage(image=hau_icon)

        self.app_label = CTkLabel(self, text="",
                    width=140, height=140, 
                    text_color=AppColors.WHITE,
                    image=hau_image,
                    bg_color=AppColors.BACKGROUND0,
                    font=(AppSpec.FONT, 18))
        self.app_label.place(x=5, y=0)

        # Cam Button
        cam_icon = Image.open(self.active_icon[0])
        cam_image = ImageTk.PhotoImage(image=cam_icon)

        self.cam_btn = CTkButton(self, text="Điểm danh",cursor="hand2", text_color=AppColors.ACTIVE_TEXT,
                    anchor="w",
                    corner_radius=5,
                    hover_color=AppColors.BUTTON_HOVER,
                    fg_color=AppColors.BACKGROUND0,
                    image=cam_image,
                    width=140, height=30, 
                    font=(AppSpec.FONT, 18),
                    command=lambda: self.switch_frame(0))
        self.cam_btn.place(x=5, y=130)
        self.frame_btn.append(self.cam_btn)

        # Table Button
        table_icon = Image.open(self.deactive_icon[1])
        table_image = ImageTk.PhotoImage(image=table_icon)

        self.table_btn = CTkButton(self, text="Báo cáo",cursor="hand2", text_color=AppColors.DEACTIVE_TEXT,
                    anchor="w",
                    corner_radius=5,
                    hover_color=AppColors.BUTTON_HOVER,
                    fg_color=AppColors.BACKGROUND0,
                    image=table_image,
                    width=140, height=30, 
                    font=(AppSpec.FONT, 18),
                    command=lambda: self.switch_frame(1))
        self.table_btn.place(x=5, y=165)
        self.frame_btn.append(self.table_btn)

        # Exit Button
        exit_icon = Image.open('.\\resources\\exit_icon_1.png')
        exit_image = ImageTk.PhotoImage(image=exit_icon)

        self.exit_btn = CTkButton(self, text="Thoát",cursor="hand2", text_color=AppColors.DEACTIVE_TEXT,
                  corner_radius=5,
                  anchor="w",
                  hover_color=AppColors.RED,
                  fg_color=AppColors.BACKGROUND0,
                  image=exit_image,
                  width=140, height=30, 
                  font=(AppSpec.FONT, 18),
                  command=lambda: self.root_frame.switch_frame(0))
        # TechSupports.display_to_label(self.exit_btn, exit_icon)
        self.exit_btn.place(x=5, y=385)

    def switch_frame(self, index):
        for i in range(len(self.sub_frame)):
            if i==index:
                self.sub_frame[i].open()
            else:
                self.sub_frame[i].close()

        for i in range(len(self.frame_btn)):
            if i==index:
                icon = Image.open(self.active_icon[i])
                image = ImageTk.PhotoImage(image=icon)
                self.frame_btn[i].configure(text_color=AppColors.ACTIVE_TEXT, image=image)
            else:
                icon = Image.open(self.deactive_icon[i])
                image = ImageTk.PhotoImage(image=icon)
                self.frame_btn[i].configure(text_color=AppColors.DEACTIVE_TEXT, image=image)

    def reset_main(self):
        self.switch_frame(0)

    def update_summary(self, reg_face):
        self.sub_frame[1].update(reg_face)

    def close(self):
        super().close()
        self.reset_main()
        self.sub_frame[0].close_camera()

class CameraFrame(AppFrame):

    def __init__(self, root, root_frame):
        self.cam_icons = ['.\\resources\\open_cam.png', '.\\resources\\close_cam.png']
        super().__init__(root, root_frame, width=AppSpec.WIDTH-160)

        self.haar = cv2.CascadeClassifier(AppData.HAAR_PATH)
        self.face_reg = FaceRecogition()
        self.face_reg.load_models(AppData.MODEL_PATH, AppData.EMBED_PATH, AppData.CLASSES_PATH)
        self.frame_count = 0

    def setup(self):
        super().setup()
        self.configure(fg_color=AppColors.LIGHT_BLUE, height=AppSpec.HEIGHT-AppSpec.TITLE_BAR-11, width=AppSpec.WIDTH-167)

        self.camera_running = False

        self.bg_camera_label = CTkLabel(self, text="",width=567, height=320, corner_radius=10, fg_color=AppColors.WHITE, bg_color=AppColors.LIGHT_BLUE)
        self.bg_camera_label.place(x=57, y=32)

        self.camera_label = CTkLabel(self, text="",width=560, height=315, corner_radius=10, fg_color=AppColors.BLACK, bg_color=AppColors.WHITE)
        self.camera_label.place(x=60, y=35)

        cam_icon = Image.open(self.cam_icons[0])
        cam_image = ImageTk.PhotoImage(image=cam_icon)

        self.camera_btn = CTkButton(self, text="Bật", text_color=AppColors.BLACK, font=(AppSpec.FONT, 20), 
                                    image=cam_image,command=self.camera, width=100, height=35,
                                    corner_radius=10, fg_color=AppColors.GRAY,
                                    hover_color=AppColors.GREEN)
        self.camera_btn.place(x=300, y=365)

    def open_camera(self):
        if not self.camera_running:
            cam_icon = Image.open(self.cam_icons[1])
            cam_image = ImageTk.PhotoImage(image=cam_icon)
            self.camera_btn.configure(image=cam_image, text="Tắt", hover_color=AppColors.RED)

            self.camera_label.configure(corner_radius=0, fg_color=AppColors.WHITE)
            self.cap = cv2.VideoCapture(AppSpec.CAMERA_INDEX)
            self.camera_running = True
            self.update_frame()
            # self.thread = threading.Thread(target=self.update_frame)
            # self.thread.start()
    
    def update_frame(self):
        if self.camera_running:
            self.frame_count += 1
            _, frame = self.cap.read()
            frame = cv2.flip(frame, 1)

            # Recognition Area
            opencv_image = self.processing(frame)

            captured_image = Image.fromarray(opencv_image)

            TechSupports.display_to_label(self.camera_label, captured_image)

            self.camera_label.after(1, self.update_frame)

    def processing(self, frame):
        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.haar.detectMultiScale(gray_img, 1.5, 5)

        opencv_image, i_faces = self.tracking(opencv_image, faces)
        if self.frame_count == 10:
            opencv_image = self.recognizing(i_faces, opencv_image, faces)
        # if self.frame_count == 10:
        #     for x, y, w, h in faces:
        #         img = opencv_image[y:y+h, x:x+w]
        #         img = cv2.resize(img, (160, 160))
        #         img = np.expand_dims(img, axis=0)
                
        #         face_score = self.face_reg.predict_proba(img)
        #         if float(face_score) > 0.8:
        #             face_name = self.face_reg.predict(img)
                    
        #             cv2.rectangle(opencv_image, (x,y), (x+w, y+h), (255,0,255), 10)
        #             cv2.putText(opencv_image, f'{face_name}-{face_score}', (x,y-10), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 3, cv2.LINE_AA)

        #             output_image = frame
        #             cv2.rectangle(output_image, (x,y), (x+w, y+h), (255,0,255), 10)
        #             cv2.putText(output_image, f'{face_score}', (x,y-10), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 3, cv2.LINE_AA)

        #             now = datetime.now()
        #             current_time = now.strftime("%Y-%m-%d %H:%M:%S")

        #             output_dir = TechSupports.export_image(output_image, str(face_name))

        #             face_list = [reg['maso'] for reg in self.root.reg_list]
        #             if str(face_name) not in face_list:
        #                 print("hello")
        #                 self.root.reg_list.append({'maso': face_name,
        #                                         'thoigian': current_time,
        #                                         'output': output_dir})
        #                 self.root.update_summary(face_name)
        #                 # self.thread = threading.Thread(target=self.root.show_noti)
        #                 # self.thread.start()
        #                 # self.root.show_noti()
        #     self.frame_count = 0
        # else:
            # opencv_image = frame
        return opencv_image
        # return frame

    def tracking(self, image, faces):
        face_imgs = []
        for x, y, w, h in faces:
            img = image[y:y+h, x:x+w]
            img = cv2.resize(img, (160, 160))
            face_imgs.append(img)
            # img = np.expand_dims(img, axis=0)
            
            cv2.rectangle(image, (x,y), (x+w, y+h), (255,0,255), 5)
        return image, np.array(face_imgs)

    def recognizing(self, i_faces, image, faces):
        print(i_faces.shape)
        face_names = self.face_reg.predict(i_faces)
        face_scores = self.face_reg.predict_proba(i_faces)
        face_indexs = np.where(face_scores > 0.85)
        
        for i in face_indexs:
            cv2.putText(image, f'{face_names[i]}-{face_scores[i]}', (faces[i][0],faces[i][1]-10), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 3, cv2.LINE_AA)
        # for x, y, w, h in faces:
        #     img = image[y:y+h, x:x+w]
        #     img = cv2.resize(img, (160, 160))
        #     img = np.expand_dims(img, axis=0)
            
        #     cv2.rectangle(image, (x,y), (x+w, y+h), (255,0,255), 5)
        return image

    def close_camera(self):
        if self.camera_running:
            cam_icon = Image.open(self.cam_icons[0])
            cam_image = ImageTk.PhotoImage(image=cam_icon)
            self.camera_btn.configure(image=cam_image, text="Bật", hover_color=AppColors.GREEN)

            self.camera_running = False
            self.cap.release()  # Release the camera

            # Display a black blank frame
            TechSupports.blank_label(self.camera_label)

    def camera(self):
        if not self.camera_running:
            self.open_camera()
        else:
            self.close_camera()

    def open(self):
        self.place(x=150, y=0)

    def close(self):
        super().close()

class SummaryFrame(AppFrame):

    def __init__(self, root, root_frame):
        super().__init__(root, root_frame)
        self.items = []

    def setup(self):
        super().setup()
        self.configure(fg_color=AppColors.LIGHT_BLUE, height=AppSpec.HEIGHT-AppSpec.TITLE_BAR-11, width=AppSpec.WIDTH-167)
        
        self.header_frame = CTkFrame(self, height=40, width=565, fg_color=AppColors.GRAY)
        self.header_frame.place(x=60, y=35)

        self.name_label = CTkLabel(self.header_frame, text = "Mã điểm danh",height=30, width=200, fg_color=AppColors.GRAY, font=(AppSpec.FONT, 18, "bold"), text_color=AppColors.DARK_BLUE, corner_radius=2)
        self.name_label.place(x=5, y=5)

        self.time_label = CTkLabel(self.header_frame, text="Thời gian điểm danh",height=30, width=300, fg_color=AppColors.GRAY, font=(AppSpec.FONT, 18, "bold"), text_color=AppColors.DARK_BLUE, corner_radius=2)
        self.time_label.place(x=210, y=5)

        self.table_frame = CTkScrollableFrame(self, width=560, height=300, fg_color=AppColors.BACKGROUNDTABLE)
        self.table_frame.place(x=55, y=70)

    def open(self):
        super().open()
        self.place(x=150, y=0)

    def update(self, item):
        TableItem(item, self.table_frame)

    def close(self):
        super().close()


class CustomMessageBox(CTkToplevel):
    def __init__(self, master=None, title="Message", name="", icon=None):
        super().__init__(master)
        self.title(title)
        self.geometry(f"350x160+{master.winfo_rootx()+400}+{master.winfo_rooty()}")
        self.resizable(False, False)

        if name == "":
            name = "Nhân vật mới"
            message_2="*Không tìm thấy dữ liệu phù hợp.  "
            TEXT_COLOR = "#ff0000"
        else:
            message_2 = ""
            TEXT_COLOR = "#0F0"

        self.label_1 = CTkLabel(self, text="Chào mừng", font=("Roboto", 20, "bold"))
        self.label_1.pack(pady=(5, 0))

        self.label_2 = CTkLabel(self, text=name, font=("Roboto", 18, "bold"), text_color=TEXT_COLOR)
        self.label_2.pack(pady=(0))

        self.label_3 = CTkLabel(self, text="đến với Khoa Công nghệ thông tin!", font=("Roboto", 20, "bold"))
        self.label_3.pack(pady=(0))

        if icon:
            self.icon_image = ImageTk.PhotoImage(Image.open(icon))
            self.icon_label = CTkLabel(self, image=self.icon_image, text="", height=50, width=200)
            self.icon_label.pack(padx=10)

        self.label_4 = CTkLabel(self, text=message_2, font=("Roboto", 11, "italic"), width=200, text_color="#ff0000")
        self.label_4.pack(pady=(5, 10))

        self.center_window()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')