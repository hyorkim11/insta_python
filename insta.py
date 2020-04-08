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
structure the program like the following:
1. check if roster exists
2. give choices to log in as any one of them
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

img_tracker = 0

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

while(1):
	print("insta.py root loop")
	# LOGIN SETUP ###########################
	username = input("username: ")
	pw = ""
	if username == "0":
		print("insta.py shut-down")
		break;

	# FIND matching password for username
	print("retrieving login credentials to check...")
	for tup in roster:
		if tup[0] == username:
			pw = tup[1]
	if not pw:
		print("#####ERROR: ##### failed to locate a matching password for that username.")
		pw = getpass.getpass("pw manual-entry: ")
	
	# FIND matching caption hashtags for username
	try:
		account_caption = " " + roster_caption[username]
		print("account caption successfully matched and pulled.")

		# MAIN LOGIC ################
		api = InstagramAPI(username, pw)
		if (api.login()):
			# api.getSelfUserFeed()  # get self user feed
			print("Logged in as: " + username)
			while(1):
				# MAIN FRAME
				print(menuText)
				cmd = input()
				if (cmd == "0"):
					print("Logging out of user")
					img_tracker = 0
					break
				elif (cmd == "1"):
					# upload a singe photo
					# images must be called "[#].jpg"
					print("photopath by default in current pwd. file name 1.jpg")
					photo_path = "1.jpg"
					unique_caption = input("type UNIQUE caption: ")
					print("WARNING: uploading image to: "+ username + "'s account\n Y/N")
					ans = input()
					if (ans == 'Y' or 'y'):
						try:
							api.uploadPhoto(photo_path, caption=unique_caption + account_caption)	
							pass
						except Exception as e:
							raise
						else:
							print("Image upload FAILED!")
							pass
						finally:
							print("Image upload success!")
							img_tracker = img_tracker+1
							# os.remove(photo_path)
							shutil.move("1.jpg", myPath+"/GDrive_upload/"+username+"_"+str(img_tracker)+".jpg")
							pass
					else:
						print("upload image aborted.")
				elif (cmd == "vid"):
					print("Upload video 1.mp4 with 1.jpg thumbnail")
					video_path = "1.mp4"
					unique_caption = input("type UNIQUE Caption: ")
					unique_caption+= account_caption
					print("WARNING: Uploading 1.mp4 and 1.jpg to: "+ username + "'s account\n Y/N")
					ans = input()
					# media = {
					# 	'type':'video',
					# 	'file':'1.mp4',
					# 	'thumbnail':'1.jpg'
					# }
					if (ans == "Y" or "y"):
						api.uploadVideo("1.mp4", "1.jpg", caption=unique_caption)
						print("Video upload success!")
					else:
						print("upload image aborted")
				elif (cmd == "2"):
					print("Album upload with the files in the current directory")
					# grab number of .jpg files at runtime
					# REQUIRES more than 1 jpg file in PWD
					img_counter = len(glob.glob1(myPath,"*.jpg"))
					media = [{
						'type': 'photo',
						'file': '1.jpg',
					}]
					for idx in range(2, img_counter+1):
						media.append({'type':'photo', 'file':'{}.jpg'.format(idx)})
					unique_caption = input("enter unique album caption: ")
					try:
						api.uploadAlbum(media, caption = unique_caption + account_caption)
						print("Album upload complete")
					except Exception as e:
						print("ERROR: something went wrong trying to upload album.")
						raise
					finally:
						for idx in range(1, img_counter+1):
							print("Cleaning up files..." + str(idx) + "/" + str(img_counter))
							# os.remove('{}.jpg'.format(idx))
							shutil.move(str(idx)+'.jpg', myPath+"/GDrive_upload/"+username+"_"+str(img_tracker)+".jpg")
							img_tracker = img_tracker+1
						pass
				elif (cmd == "3"):
					# upload batch of 6 images.
					# images MUST BE named "1.jpg" ~ "6.jpg"
					print("batch of 6 upload for new clients!")
					try:
						for idx, imageFileName in enumerate(batchList, 1):
							photo_path = imageFileName
							api.uploadPhoto(photo_path, caption=account_caption)
							print("Image " + str(idx) + " upload complete")
							os.remove(photo_path)
						print("Batch upload complete")
					except Exception as e:
						print("batch upload failed. Check file names and file count")
						raise
				elif (cmd == "4"):
					# SWITCH SNS ACCOUNTS
					print("Saved for multi accounts")
				elif (cmd == "7"):
					print("this command is reserved for testing")
				elif (cmd == "8"):
					# call Google Sheets API, filter lists for valid data
					# returns a list of lists ['ID', 'PW']
					print("Running Google Sheets API to retrieve roster of login-info...")
					roster = sheets.clean_values(sheets.sheets_setup())
					with open("roster.txt", "wb") as fp:
						print("roster update complete.")
						pickle.dump(roster, fp)
				elif (cmd == "9"):
					pp.pprint(api.getSelfUserFeed())
			api.logout()
		else:
				print("Can't login!")
	except Exception as e:
		account_caption = ""
		print("##### WARNING: ##### failed to locate a matching account caption.")
	finally:
		pass
'''
uploading video as part of album
# {
    #    'type'     : 'video',
    #    'file'     : '/path/to/your/video.mp4', # Path to the video file.
    #    'thumbnail': '/path/to/your/thumbnail.jpg'
    # }
'''