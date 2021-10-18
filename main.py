from web_controller import WebController
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Create an instance of our web controller class
wc = WebController()

wc.start_record()

wc.driver.close()