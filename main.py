from web_controller import WebController
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Create an instance of our web controller class
wc = WebController()

df = pd.DataFrame()
num_iter = 1
# df["list_base"] = wc.start_record_list_base(num_iter)
# df["list_png"] = wc.start_record_list_png(num_iter)

wc.driver.close()