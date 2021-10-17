from selenium import webdriver
from .which_developer import DEV_NAME
import time
from binascii import a2b_base64
import pyexiv2
import base64
import io
import numpy as np
from PIL import Image
import numpy.linalg as la
import os
import keyboard

class WebController:

    # Creates the object and handles if this is running on alex's or scotts computer
    def __init__(self,init_load=True):

        # Create the driver based on what computer is running this code
        if DEV_NAME == "alex":
            self.driver = webdriver.Chrome()
        elif DEV_NAME == "scott":
            self.driver = webdriver.Chrome()
        else:
            raise ValueError(f"Unknown dev name in which_developer: {DEV_NAME}")

        # Other variables
        self.rgb_weights = 1/3 * np.ones(3)
        self.pixel_ratio = self.driver.execute_script("return window.devicePixelRatio")
        # Load up max dirt bike
        if init_load:
            self.init_load()


    def init_load(self):
        self.driver.get("https://cdn3.addictinggames.com/addictinggames-content/ag-assets/content-items/html5-games/maxdirtbike/index.html?unprocessed=true")
        self.canvas = self.driver.find_element_by_tag_name("canvas")

        # # Wait for game to start
        # self.canvas = self.driver.find_element_by_tag_name("canvas")
        # canvas_diff = np.inf
        # start_menu_data = np.array(Image.open('img/start_menu.jpg')).astype(int)
        # while canvas_diff > 8000:
        #     img = self.get_canvas_img()
        #     img_data = np.array(img)
        #     canvas_diff = la.norm(start_menu_data-img_data)
        #     # print(canvas_diff)

    def get_canvas_img(self):
        screen_data = base64.b64decode(self.driver.get_screenshot_as_base64())
        image = Image.open(io.BytesIO(screen_data))
        image = image.convert("L") # Convert to greyscale
        image.save("canvas_pre.jpg", "JPEG")
        image = image.crop((self.canvas.location["x"]*self.pixel_ratio,
                            self.canvas.location["y"]*self.pixel_ratio,
                            self.canvas.location["x"]*self.pixel_ratio+self.canvas.size["width"]*self.pixel_ratio,
                            self.canvas.location["y"]*self.pixel_ratio+self.canvas.size["height"]*self.pixel_ratio))
        image.save("canvas_post.jpg", "JPEG")
        return image.resize((300,300))

    def start_record(self):
        run_number = np.random.randint(1000,9999)
        foldername = f"img/Run Data/run_{run_number}/"
        while os.path.isfile(foldername):
            run_number = np.random.randint(1000,9999)
            foldername = f"run_{run_number}/"
        os.mkdir(foldername)
        print(f"Recording started with run number {run_number}")
        count = 0
        try:
            while True:
                img = self.get_canvas_img()
                img.save(foldername + f"{count}.jpg", "JPEG")
                img_data = pyexiv2.Image(foldername + f"{count}.jpg")
                # Add input to image data
                # space,left,right,up,down
                key_info = np.array([0,0,0,0,0])
                if keyboard.is_pressed('space'):
                    key_info[0] = 1
                if keyboard.is_pressed('left'):
                    key_info[1] = 1
                if keyboard.is_pressed('right'):
                    key_info[2] = 1
                if keyboard.is_pressed('up'):
                    key_info[3] = 1
                if keyboard.is_pressed('down'):
                    key_info[4] = 1
                img_data.modify_comment("".join(key_info.astype(str)))
                count+=1
        except:
            print(f"Recording ended. {count} images saved!")