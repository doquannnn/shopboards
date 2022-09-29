from PIL import Image
import requests
from io import BytesIO
import numpy as np
import os

with open("text.txt") as f:
    elements = f.read().split("\n")

stores = set()
base = "http://nutifood.dmsone.vn:8080/dmsone"
i = 0

for element in elements:
    try:
        store, image_url, _ = element.split(",")
    except ValueError:
        break
    i += 1

    store = store[2:-1]

    if store not in stores:
        os.mkdir(store)
        stores.add(store)
    url = f"{base}{image_url[2:-1]}"

    response = requests.get(url)

    try:
        img = Image.open(BytesIO(response.content))
    except:
        pass

    img_name = image_url.split("/")[-1]
    # print(img_name)
    #     print(i)
    os.chdir(store)
    img.save(f"{img_name}.jpg")
    os.chdir("..")

print(i)
