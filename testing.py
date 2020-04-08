#!/usr/bin/env python
# -*- coding: utf-8 -*-

from InstagramAPI import InstagramAPI
from client_data import roster_caption
import getpass
import os
import glob
import sheetsapi as sheets
import driveapi as drive
import pickle
import pprint
import argparse
import shutil


'''###################################
TODO:
Optimize code structure for every command

since i have the login-roster
structure the program like so:
1. check if roster exists
2. give choice to log in as any one of them
3. depending on the ID, have a separate folder to put their image files
4. script goes down the list and logs in each account, checks respective folder for images
5. determines if its a single photo/album and uploads

NOTES:
- 'zip' library for multi-simultaneous iteration over lists for acc/pwd lists
- test uploading video as part of album (code piece at EOF)
- 'curses' library for interactivity
- 'tkinter' library for GUI
- 'py2app' library to create standalone mac app from python project
- 'crontab' library for cronjobs
- 'pillow' library for adding logos to images
https://docs.eyesopen.com/toolkits/cookbook/python/image-manipulation/addlogo.html

###################################'''

# DEFINE GLOBALS  ###########
# Batch image file names
batchList = ["1.jpg","2.jpg","3.jpg","4.jpg","5.jpg","6.jpg"]
menuText = """
#### Main Menu ####
Please type in appropriate command #:

1. Upload New Image
2. Upload New Album
3. Upload New Account Images (Batch of 6)
4. Switch Account
7. Reserved Testing
8. Update Login Info Roster
9. Print Account Stream
0. Logout/End Script
###################
"""

parser = argparse.ArgumentParser()
parser.add_argument('-u', action='store_true', default=False, dest='u')

# Initialize json prettyprint
pp = pprint.PrettyPrinter(indent=2)

# call Google Sheets API, filter lists for valid data
# returns a list of lists ['ID', 'PW']
print (parser.parse_args().u)

if parser.parse_args().u == True:
	print("Detected Update flag in command. \n Updating login roster...")
	roster = sheets.clean_values(sheets.sheets_setup())
	with open("roster.txt", "wb") as fp:
		print("roster update complete.")
		pickle.dump(roster, fp)

# Roster filter
def prettyRoster(roster):
	for x in roster:
		print(x)

# ERROR CHECKING: .jpg FILECOUNT in pwd
myPath = os.path.dirname(os.path.realpath(__file__))
if len(glob.glob1(myPath,"*.jpg")) == 0:
	print("##### WARNING: ##### No .jpg files were found in this folder!")

with open("roster.txt", "rb") as fp:
	try:
		roster = pickle.load(fp)
		print("Current Roster: ")
		arranged = tuple(roster)
		arranged = (sorted(arranged, key=lambda account: account[0]))
		for tup in arranged:
			print("\t " + tup[0])

	except:
		print("##### ERROR: ##### failed to load roster file.")
	finally:
		pass

print("moving file")
try:
	shutil.move("1.jpg", myPath+"/GDrive_upload/")
except:
	account_IMG_counter = 1
	shutil.move("1.jpg", myPath+"/GDrive_upload/"+str(account_IMG_counter+1)+".jpg")
