from selenium import webdriver
import time
import base64
import io
import numpy as np
from PIL import Image
import os
import keyboard

class WebController:

    # Creates the object and handles if this is running on alex's or scotts computer
    def __init__(self,init_load=True):

        # Create the driver based on what computer is running this code

        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome('chromedriver', chrome_options=chrome_options)

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
        image = image.crop((self.canvas.location["x"]*self.pixel_ratio,
                            self.canvas.location["y"]*self.pixel_ratio,
                            self.canvas.location["x"]*self.pixel_ratio+self.canvas.size["width"]*self.pixel_ratio,
                            self.canvas.location["y"]*self.pixel_ratio+self.canvas.size["height"]*self.pixel_ratio))
        return image.resize((300,300))

    def get_current_inputs(self):
        # Add input to image data
        # space,left,right,up,down
        key_info = ""
        if keyboard.is_pressed('space'):
            key_info += "1"
        else:
            key_info += "0"
        if keyboard.is_pressed('left'):
            key_info += "1"
        else:
            key_info += "0"
        if keyboard.is_pressed('right'):
            key_info += "1"
        else:
            key_info += "0"
        if keyboard.is_pressed('up'):
            key_info += "1"
        else:
            key_info += "0"
        if keyboard.is_pressed('down'):
            key_info += "1"
        else:
            key_info += "0"
        return key_info + "\n"

    def start_record(self):
        run_number = np.random.randint(1000,9999)
        foldername = f"img/Run Data/run_{run_number}/"
        while os.path.isfile(foldername):
            run_number = np.random.randint(1000,9999)
            foldername = f"run_{run_number}/"
        os.mkdir(foldername)
        print(f"Recording started with run number {run_number}")

        img_list = []
        key_info = ""

        try:
            start_time = time.time()
            while True:
                img_list.append(self.get_canvas_img())
                key_info += self.get_current_inputs()
        except:
            total_time = time.time()-start_time
            count = len(img_list)
            print("Recording ended.")
            print(f"Avg frames/sec : {count/total_time}")
            print(f"Saving {count} images...",end="")
            for i in range(count):
                img_list[i].save(foldername + f"{i}.jpg", "JPEG")
            open(foldername +"key_info.txt",'w').write(key_info)
            print("DONE!")


    def start_record_list(self,num_iters):
        run_number = np.random.randint(1000,9999)
        foldername = f"img/Run Data/run_{run_number}/"
        while os.path.isfile(foldername):
            run_number = np.random.randint(1000,9999)
            foldername = f"run_{run_number}/"
        os.mkdir(foldername)
        print(f"Recording started with run number {run_number}")

        times = np.zeros(num_iters)
        img_list = []
        key_info = ""
        for i in range(num_iters):
            start_time = time.time()
            img_list.append(self.get_canvas_img())
            key_info += self.get_current_inputs()
            times[i] = time.time() - start_time

        count = len(img_list)
        print("Recording ended.")
        print(f"Saving {count} images...",end="")
        for i in range(count):
            img_list[i].save(foldername + f"{i}.jpg", "JPEG")
        open(foldername +"key_info.txt",'w').write(key_info)
        print("DONE!")

        return times

    def start_record_save(self,num_iters):
        run_number = np.random.randint(1000, 9999)
        foldername = f"img/Run Data/run_{run_number}/"
        while os.path.isfile(foldername):
            run_number = np.random.randint(1000, 9999)
            foldername = f"run_{run_number}/"
        os.mkdir(foldername)
        print(f"Recording started with run number {run_number}")

        times = np.zeros(num_iters)
        key_info = ""

        for i in range(num_iters):
            start_time = time.time()
            self.get_canvas_img().save(foldername + f"{i}.jpg", "JPEG")
            key_info += self.get_current_inputs()
            times[i] = time.time() - start_time

        print("Recording ended.")
        print(f"Saving {num_iters} images...", end="")
        open(foldername + "key_info.txt", 'w').write(key_info)
        print("DONE!")

        return times

    def start_record_list_base(self,num_iters):
        run_number = np.random.randint(1000, 9999)
        foldername = f"img/Run Data/run_{run_number}/"
        while os.path.isfile(foldername):
            run_number = np.random.randint(1000, 9999)
            foldername = f"run_{run_number}/"
        os.mkdir(foldername)
        print(f"Recording started with run number {run_number}")

        times = np.zeros(num_iters)
        img_list = []
        key_info = ""

        for i in range(num_iters):
            start_time = time.time()
            img_list.append(self.driver.get_screenshot_as_base64())
            key_info += self.get_current_inputs()
            times[i] = time.time() - start_time

        count = len(img_list)
        print("Recording ended.")
        print(f"Saving {count} images...", end="")
        for i in range(count):
            screen_data = base64.b64decode(img_list[i])
            image = Image.open(io.BytesIO(screen_data))
            image = image.convert("L")  # Convert to greyscale
            image = image.crop((self.canvas.location["x"] * self.pixel_ratio,
                                self.canvas.location["y"] * self.pixel_ratio,
                                self.canvas.location["x"] * self.pixel_ratio + self.canvas.size[
                                    "width"] * self.pixel_ratio,
                                self.canvas.location["y"] * self.pixel_ratio + self.canvas.size[
                                    "height"] * self.pixel_ratio))
            image = image.resize((300, 300))
            image.save(foldername + f"{i}.jpg", "JPEG")
        open(foldername + "key_info.txt", 'w').write(key_info)
        print("DONE!")

        return times

    def start_record_list_png(self,num_iters):
        run_number = np.random.randint(1000, 9999)
        foldername = f"img/Run Data/run_{run_number}/"
        while os.path.isfile(foldername):
            run_number = np.random.randint(1000, 9999)
            foldername = f"run_{run_number}/"
        os.mkdir(foldername)
        print(f"Recording started with run number {run_number}")

        times = np.zeros(num_iters)
        img_list = []
        key_info = ""

        for i in range(num_iters):
            start_time = time.time()
            img_list.append(self.driver.get_screenshot_as_png())
            key_info += self.get_current_inputs()
            times[i] = time.time() - start_time

        count = len(img_list)
        print("Recording ended.")
        print(f"Saving {count} images...", end="")
        for i in range(count):
            image = Image.open(io.BytesIO(img_list[i]))
            image = image.convert("L")  # Convert to greyscale
            image = image.crop((self.canvas.location["x"] * self.pixel_ratio,
                                self.canvas.location["y"] * self.pixel_ratio,
                                self.canvas.location["x"] * self.pixel_ratio + self.canvas.size[
                                    "width"] * self.pixel_ratio,
                                self.canvas.location["y"] * self.pixel_ratio + self.canvas.size[
                                    "height"] * self.pixel_ratio))
            image = image.resize((300, 300))
            image.save(foldername + f"{i}.jpg", "JPEG")
        open(foldername + "key_info.txt", 'w').write(key_info)
        print("DONE!")

        return times
