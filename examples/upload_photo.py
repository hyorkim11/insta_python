#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Use text editor to edit the script and type in valid Instagram username/password

from InstagramAPI import InstagramAPI

InstagramAPI = InstagramAPI("hyorimmmm", "Godisgood1")
InstagramAPI.login()  # login

photo_path = '/Desktop/sampling.jpg'
caption = "Sample photo from my python script!"
InstagramAPI.uploadPhoto(photo_path, caption=caption)
