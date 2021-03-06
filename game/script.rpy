﻿# You can place the script of your game in this file.
init:  
    # Here all the background & character images are loaded!
    # Put them in the folder backgrounds or chacters respectively
    # the resulting tags will be:
    # for backgrounds it starts with bg, then the names of the folder in which the image is placed and lastly the  name of the file
    # same for character
    # so for example character/eileen/happy.png will become ch eileen happy
    python:
        load_images("backgrounds", "bg") # load all images
        load_images("characters") # load all images
        load_chars() # load all characters, from characters.rpy

#init python for nvl mode
init python:
    config.empty_window = nvl_show_core
    config.window_hide_transition = dissolve
    config.window_show_transition = dissolve
# The game starts here.
label start:
    call chapter_1
    call chapter_2
    call chapter_3
    call chapter_4
    call chapter_5
    call chapter_6
    return
