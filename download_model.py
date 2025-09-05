import gdown
import os

FILE_ID = "1_Ku5FTHIldn4CRS9-46ijfhOqWh8l5_M"
URL = f"https://drive.google.com/uc?id={FILE_ID}"
OUTPUT = "similarity.pkl"

if not os.path.exists(OUTPUT):
    print("Downloading similarity.pkl from Google Drive…")
    gdown.download(URL, OUTPUT, quiet=False)
else:
    print("similarity.pkl already exists.")
