import os

import json

all_pictures = os.listdir("slides")



for index, pic in enumerate(all_pictures):
    os.rename(os.path.join("slides", pic), f"slides/slide_{index + 1}.png")
        
    

