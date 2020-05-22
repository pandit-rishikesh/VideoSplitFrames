#!/usr/bin/python3

# This program creates a directory tree under code directory and
# automatically splits the video into RGB and GrayScale frames.
# All the events executed in this program are stored in events.log in "Lesson_1" dir

# Created by: Dr. Rishikesh Pandit, Department of Physics, University of Roma Tre 
# Date Created: 2020-05-21


## Importing required modules!
import os                   # Operating System Control
import sys                  # Python System Control
import logging              # Creating and Maintaining Logfile
import shutil               # Copying and Moving Files (Shell Utilities)

try:
  import cv2                # Open Source Computer Vision Library 
except ModuleNotFoundError:
  print("OpenCV module is needed for this program\n\nFOR pip : pip install opencv-python\nFor conda: conda install -c menpo opencv ")
  sys.exit()

try:
  from PIL import Image     # Python Imaging Library (Editing/Converting ImageFiles)
except ModuleNotFoundError:
  print("Python Imaging Library needed for this program\n\nFor pip users: pip install Pillow\nFor conda users: conda install -c anaconda pillow")
  sys.exit()

## Basic Logging Configuration
logging.basicConfig(format="%(asctime)s\t%(levelname)s\t%(message)s",
                    filename="events.log", level=logging.INFO)    

logging.info("**************** New Execution Started! ******************")


codedir = os.getcwd()
os.chdir(f"{codedir}")

## Creating Lesson_1 Directoty and Locating Video File
logging.info("Creating Lesson_1 directory")
try:
 os.makedirs(f"{codedir}/Lesson_1/data")
 print("Lesson_1 Directory Created")
except FileExistsError:
 logging.error("Lesson_1 already exists!")

dirpath = f"{codedir}/Lesson_1"
os.chdir(dirpath)
print(f"current working dir changed to {dirpath}")

try:
  os.makedirs(f"{dirpath}/data")
  print("Data Directory Created")
except FileExistsError:
  logging.error(f"{dirpath}/data already exists!")

print(f"Copying video file to {dirpath}/data")

pathtovideofile = f"{codedir}/Neuroburst.mp4" # replace "Neuroburst" with video you want to split into frames

try:
  shutil.copyfile(pathtovideofile, "data/video_sample.mp4")
  print(f"Video file copied to {dirpath}/data successfully!")
except FileNotFoundError:
  print("***** Video Not Found! Please import videofile in code directory and rerun! *****")
  logging.critical("!!!! Video Not Found! Exiting Program! !!!!")
  os.chdir(f"{codedir}")
  print(f"current working dir changed to {codedir}")
  sys.exit()


print("****** Preparing to Split Frames *******")
## Split Frame and Convert GrayScale Functions

def split_frames(vid_in_path, image_out_path):

  vidcap = cv2.VideoCapture(vid_in_path)

  success, image = vidcap.read()

  count = 0

  while success:
    num = f"{count}".zfill(3)
    cv2.imwrite(f"{image_out_path}/frame_{num}.png", image)
    success, image = vidcap.read()
    count+=1

  return

def gray_scale_convert(image_in_path, gs_out_path):

  img = Image.open(image_in_path).convert('LA')
  img.save(gs_out_path)
  return


## Creating Sub-directories for images
print("Creating sub-directories for split image frames!")
try:
  os.makedirs(f"{dirpath}/split_frames/rgb")
  os.makedirs(f"{dirpath}/split_frames/gs")
except FileExistsError:
  logging.error("Image directories already exist!")

rgbpath= f"{dirpath}/split_frames/rgb"
graypath = f"{dirpath}/split_frames/gs"

print("Splitting frames using OpenCV function")

if os.path.exists(f"{rgbpath}/frame_000.png"):
  logging.error(f"Frames already exist in {rgbpath}/frame_number.png")
else:
  split_frames(f"{dirpath}/data/video_sample.mp4", f"{rgbpath}")
  print("Frames are now ready!")

## Function to upload image frames to Dictionary
def img_to_dict(imgdict, count, imgpath):
  img = cv2.imread(imgpath)
  imgdict[count] = img
  return

RGB_Dictionary = dict()
GS_Dictionary = dict()

for paths, dirs, files in (os.walk(rgbpath)):
  num = len(files)

print(f"Total number of frames split: {num}")


## Gray Scale Coversion Process! Be Patient! :)

if os.path.exists(f"{graypath}/grayframe_000.png"):
  logging.warning(f"GrayFrames already stored in {graypath}! Exiting Program!")
else:
  print(f"Converting {num} RGB frames to GrayScale")

  nfiles=0
  while(nfiles<num):
    i = f"{nfiles}".zfill(3)
    gray_scale_convert(f"{rgbpath}/frame_{i}.png", 
                     f"{graypath}/grayframe_{i}.png")

    img_to_dict(RGB_Dictionary, nfiles, f"{rgbpath}/frame_{i}.png")
    img_to_dict(GS_Dictionary, nfiles, f"{graypath}/frame_{i}.png")
    nfiles+=1
  
  print(f"{num} GrayScale frames now stored in {graypath}")

  logging.info(f"Images stored in dictionaries! Program run successful!")

os.chdir(f"{codedir}")
print("DONE! Program Run Success!")

