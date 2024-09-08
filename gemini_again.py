import tkinter as tk
from tkinter import filedialog
import pandas as pd
import os
from PIL.ExifTags import TAGS
from PIL import Image

df = pd.DataFrame(columns=["Image", "Folder address", "Coordinates"])
row = 0
lat = []
lat_ref = []
lon = []
lon_ref = []
# Open the image file
def read_data(image):
    image = Image.open(image)

    # Make a collection of properties and values corresponding to your image.
    exif = {}
    if image._getexif() is not None:
        for tag, value in image._getexif().items():
            if tag in TAGS:
                exif[TAGS[tag]] = value

    if "GPSInfo" in exif:
        gps_info = exif["GPSInfo"]

        def convert_to_degrees(value):
            d = float(value[0])
            m = float(value[1])
            s = float(value[2])
            return d + (m / 60.0) + (s / 3600.0)

        # Convert latitude and longitude to degrees
        lat = convert_to_degrees(gps_info[2])
        lon = convert_to_degrees(gps_info[4])
        lat_ref = gps_info[1]
        lon_ref = gps_info[3]

        # Adjust the sign of the coordinates based on the reference (N/S, E/W)
        if lat_ref != "N":
            lat = -lat
        if lon_ref != "E":
            lon = -lon

        # Format the GPS coordinates into a human-readable string
        geo_coordinate = "{0}° {1}, {2}° {3}".format(lat, lat_ref, lon, lon_ref)
    else:
        print("No GPS information found.")
        geo_coordinate = "{0}° {1}, {2}° {3}".format('0', '0','0','0')
    return geo_coordinate
def select_folder():
    """Selects a folder using a file dialog, adds image paths to a DataFrame,
       and saves the DataFrame as a CSV file in the same directory."""

    root = tk.Tk()
    root.withdraw()

    folder_path = filedialog.askdirectory()
    if folder_path:
        #df = pd.DataFrame(columns=["Image", "Folder address"])
        row = 0
        for index, filename in enumerate(os.listdir(folder_path)):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):  # Adjust file extensions as needed
                image_path = os.path.join(folder_path, filename)
                read_data(image_path)
                df.at[index, 'Image'] = filename
                df.at[index, 'Folder address'] = image_path
                geo_cordinate = read_data(image_path)
                df.at[index, 'Coordinates'] = geo_cordinate
        print("Folder path", folder_path)
        return folder_path

folder_path = select_folder()
# Save the CSV file

csv_file_path = folder_path + "/data.csv"  # Use forward slash for path separators
df.to_csv(csv_file_path, sep=',')

# Save the TXT file (optional)
txt_file_path = folder_path + "/data.txt"
df.to_csv(txt_file_path, sep=',', index=False)  # Remove index for TXT format

print("We have finished")
