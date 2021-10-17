from selenium import webdriver
from .which_developer import DEV_NAME
import time
from binascii import a2b_base64
import base64
import io
import numpy as np
from PIL import Image
import numpy.linalg as la

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

        # Wait for game to start
        canvas = self.driver.find_element_by_tag_name("canvas")
        canvas_diff = np.inf
        start_menu_data = np.array(Image.open('img/start_menu.jpg')).astype(int)
        while canvas_diff > 8000:
            img = self.get_canvas_img(canvas)
            img_data = np.array(img)
            canvas_diff = la.norm(start_menu_data-img_data)
            print(canvas_diff)

    def get_canvas_img(self,canvas):
        screen_data = base64.b64decode(self.driver.get_screenshot_as_base64())
        image = Image.open(io.BytesIO(screen_data))
        image = image.convert("L") # Convert to greyscale
        image.save("canvas_pre.jpg", "JPEG")
        image = image.crop((canvas.location["x"]*self.pixel_ratio,
                            canvas.location["y"]*self.pixel_ratio,
                            canvas.location["x"]*self.pixel_ratio+canvas.size["width"]*self.pixel_ratio,
                            canvas.location["y"]*self.pixel_ratio+canvas.size["height"]*self.pixel_ratio))
        image.save("canvas_post.jpg", "JPEG")
        return image.resize((300,300))

    def init_load_old(self):

        # load site
        self.driver.get("https://www.gamepix.com/play/max-dirt-bike")

        # Accept notice
        accept_btns = self.driver.find_elements_by_class_name("iubenda-cs-accept-btn")
        num_trys = 0
        while len(accept_btns) ==0:
            time.sleep(1)
            accept_btns = self.driver.find_elements_by_class_name("iubenda-cs-accept-btn")
            num_trys +=1
            # raise error if time out
            if num_trys>10:
                raise RuntimeError("Failed to find accept button")
        accept_btns[0].click()

        # Press play game
        try:
            self.driver.find_elements_by_class_name("playButtonCookieConsent")[1].click()
        except:
            raise RuntimeError("Failed to find play game button")


        # Exit ad if there is one
        num_trys = 0
        while num_trys < 10:
            try:
                self.driver.find_elements_by_class_name("videoAdUiSkipButton").click()
                print(num_trys)
                break
            except:
                print("Failed to find ad")
                time.sleep(1)
                num_trys+=1


        # Wait for game to start
        canvas = self.driver.find_element_by_tag_name("canvas")
        canvas.wi
        canvas_fidelity = 0
        while canvas_fidelity < 1:
            # canvas_data = self.driver.execute_script("return arguments[0].toDataURL('image/jpeg', 0.1).substring(22);", canvas)
            canvas_base64 = self.driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);",
                                                       canvas)

            # decode
            canvas_png = base64.b64decode(canvas_base64)

            # save to a file
            with open(r"canvas.png", 'wb') as f:
                f.write(canvas_png)
        print(0)