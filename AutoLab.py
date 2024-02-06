from tkinter import Tk, Label, Button
from PIL import Image, ImageTk
import glob
import os
from boundigbox import BoundingBoxApp

class AutoAnnotationApp:
    def __init__(self, root, data_path, folder_save_path, width, height,start_index, naming_prefix,index_length, file_extension="*.jpg"):
        self.root = root
        self.data_path =data_path
        self.folder_save_path = folder_save_path
        self.nameing_prefix = naming_prefix
        self.width = width
        self.start_index = start_index
        self.height = height
        self.file_extension = file_extension
        self.current_index = 0
        self.current_file = ""
        self.all_images = self.get_images_from_folder()
        self.index_length = index_length
        self.root.title("AUTOLAB")
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.bind("<Configure>", self.on_window_resize)

        self.image_inspector_window = None
        

        self.label_img_name = Label(root, text="")
        self.label_img_name.grid(row=1, column=0, columnspan=2, pady=10)

        self.prev_button = Button(root, text="Previous", command=self.prev_image)
        self.prev_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.next_button = Button(root, text="Next", command=self.next_image)
        self.next_button.grid(row=2, column=1, padx=10, pady=10)

        self.update_image_label()

    def get_images_from_folder(self):
        
        search_pattern = os.path.join(self.data_path, self.file_extension)
        image_files = glob.glob(search_pattern)
        return image_files

    def next_image(self):
        self.current_index = (self.current_index + 1) % len(self.all_images)
        self.update_image_label()

    def prev_image(self):
        self.current_index = (self.current_index - 1) % len(self.all_images)
        self.update_image_label()

    def update_image_label(self):
        image_path = self.all_images[self.current_index]
        self.current_file = os.path.basename(image_path)
        self.label_img_name.config(text=self.current_file)
        self.update_image(image_path)

    def update_image(self, image_path):
        image_path = image_path.replace("\\", "/")

        image = Image.open(image_path)
        
        thumbnail = image.copy()
        thumbnail.thumbnail((self.width, self.height))
        if self.image_inspector_window:
            self.image_inspector_window.update_image(thumbnail, self.current_index)
        else:
            self.image_inspector_window = BoundingBoxApp(self.root, thumbnail, self.folder_save_path, self.start_index,self.index_length, self.nameing_prefix)

    def on_window_resize(self, event):
        pass

if __name__ == "__main__":
    PROJECT = "AutoAnnotation"
    SUB_PROJECT = "auto_labels"
    VIDEO_PATH = "TEST.mp4"
    DATA_FOLDER = "images_test_cropped"
    LABEL_PATH = f"{PROJECT}/{SUB_PROJECT}/labels"
    INDEX_LENGTH = 6
    root = Tk()
    start_page = AutoAnnotationApp(root, 
                                    data_path=DATA_FOLDER,
                                    folder_save_path=LABEL_PATH,
                                    width= 1800,
                                    height= 1000,
                                    start_index=8161,
                                    index_length=INDEX_LENGTH,
                                    naming_prefix= "Norway")
    root.mainloop()


