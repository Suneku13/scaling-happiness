# This file is in the public domain. Feel free to modify it as a basis
# for your own screens.

##############################################################################
# Say
#
# Screen that's used to display adv-mode dialogue.
# http://www.renpy.org/doc/html/screen_special.html#say
screen say:

    # Defaults for side_image and two_window
    default side_image = None
    default two_window = True

    # Decide if we want to use the one-window or two-window variant.
    if not two_window:

        # The one window variant.
        window:
            id "window"

            has vbox:
                yminimum 10
                style "say_vbox"

            if who:
                text who id "who"

            text what id "what"

    else:
        # The two window variant.
        vbox:
            style "say_two_window_vbox"

            if who:
                window:
                    background "black"
                    ypos 150
                    ysize 100
                    style "say_who_window"

                    text who:
                        id "who"

            window:
                #background None
                id "window"
                ysize 150

                has vbox:
                    style "say_vbox"
                frame:
                    background "white"
                    xsize 700
                    xpos 50
                    text what id "what"

    # If there's a side image, display it above the text.
    if side_image:
        add side_image
    else:
        add SideImage() xalign 0.0 yalign 1.0

    # Use the quick menu.
    use quick_menu


##############################################################################
# Choice
#
# Screen that's used to display in-game menus.
# http://www.renpy.org/doc/html/screen_special.html#choice

screen choice:

    window:
        style "menu_window"
        xalign 0.5
        yalign 0.5

        vbox:
            style "menu"
            spacing 2

            for caption, action, chosen in items:

                if action:

                    button:
                        action action
                        style "menu_choice_button"

                        text caption style "menu_choice"

                else:
                    text caption style "menu_caption"

init -2:
    $ config.narrator_menu = True

    style menu_window is default

    style menu_choice is button_text:
        clear

    style menu_choice_button is button:
        xminimum int(config.screen_width * 0.75)
        xmaximum int(config.screen_width * 0.75)


##############################################################################
# Input
#
# Screen that's used to display renpy.input()
# http://www.renpy.org/doc/html/screen_special.html#input

screen input:

    window style "input_window":
        has vbox

        text prompt style "input_prompt"
        input id "input" style "input_text"

    use quick_menu

##############################################################################
# Nvl
#
# Screen used for nvl-mode dialogue and menus.
# http://www.renpy.org/doc/html/screen_special.html#nvl

screen nvl:

    window:
        style "nvl_window"

        has vbox:
            style "nvl_vbox"

        # Display dialogue.
        for who, what, who_id, what_id, window_id in dialogue:
            window:
                id window_id

                has hbox:
                    spacing 10

                if who is not None:
                    text who id who_id

                text what id what_id

        # Display a menu, if given.
        if items:

            vbox:
                id "menu"

                for caption, action, chosen in items:

                    if action:

                        button:
                            style "nvl_menu_choice_button"
                            action action

                            text caption style "nvl_menu_choice"

                    else:

                        text caption style "nvl_dialogue"

    add SideImage() xalign 0.0 yalign 1.0

    use quick_menu

##############################################################################
# Main Menu
#
# Screen that's used to display the main menu, when Ren'Py first starts
# http://www.renpy.org/doc/html/screen_special.html#main-menu

screen main_menu:

    # This ensures that any other menu screen is replaced.
    tag menu

    # The background of the main menu.
    window:
        background "black"
    # The main menu buttons.
    frame:
        xalign 0.5
        yalign 0.5

        hbox:
            xalign 0.5
            yalign 0.5
            #imagebutton action Start()  idle "img/start.png" insensitive "img/start.png" hover "img/start.png" selected_idle "img/start.png" selected_hover "img/start.png"
            textbutton _("Start Game") action Start()
            textbutton _("Load Game") action ShowMenu("load")
            textbutton _("Preferences") action ShowMenu("preferences")
    frame:
        xalign 0.5
        yalign 0.8
        hbox:
            xalign 0.5
            yalign 0.5
            textbutton _("Gallery") action ShowMenu("gallery")
            textbutton _("Music Room") action ShowMenu("music_room")
            #textbutton ("Help") action Help()
            textbutton _("Update") action renpy.curry(renpy.invoke_in_new_context)(updateGame)
            textbutton _("Quit") action Quit(confirm=False)

init -2:

    # Make all the main menu buttons be the same size.
    style mm_button:
        size_group "mm"



##############################################################################
# Navigation
#
# Screen that's included in other screens to display the game menu
# navigation and background.
# http://www.renpy.org/doc/html/screen_special.html#navigation
screen navigation:

    # The background of the game menu.
    window:
        style "gm_root"

    # The various buttons.
    frame:
        style_group "gm_nav"
        xalign .98
        yalign .98

        has vbox

        textbutton _("Return") action Return()
        textbutton _("Preferences") action ShowMenu("preferences")
        textbutton _("Save Game") action ShowMenu("save")
        textbutton _("Load Game") action ShowMenu("load")
        textbutton _("Main Menu") action MainMenu()
        textbutton _("Help") action Help()
        textbutton _("Quit") action Quit()

init -2:

    # Make all game menu navigation buttons the same size.
    style gm_nav_button:
        size_group "gm_nav"


##############################################################################
# Save, Load
#
# Screens that allow the user to save and load the game.
# http://www.renpy.org/doc/html/screen_special.html#save
# http://www.renpy.org/doc/html/screen_special.html#load

# Since saving and loading are so similar, we combine them into
# a single screen, file_picker. We then use the file_picker screen
# from simple load and save screens.

screen file_picker:

    frame:
        style "file_picker_frame"

        has vbox

        # The buttons at the top allow the user to pick a
        # page of files.
        hbox:
            style_group "file_picker_nav"

            textbutton _("Previous"):
                action FilePagePrevious()

            textbutton _("Auto"):
                action FilePage("auto")

            textbutton _("Quick"):
                action FilePage("quick")

            for i in range(1, 9):
                textbutton str(i):
                    action FilePage(i)

            textbutton _("Next"):
                action FilePageNext()

        $ columns = 2
        $ rows = 5

        # Display a grid of file slots.
        grid columns rows:
            transpose True
            xfill True
            style_group "file_picker"

            # Display ten file slots, numbered 1 - 10.
            for i in range(1, columns * rows + 1):

                # Each file slot is a button.
                button:
                    action FileAction(i)
                    xfill True

                    has hbox

                    # Add the screenshot.
                    add FileScreenshot(i)

                    $ file_name = FileSlotName(i, columns * rows)
                    $ file_time = FileTime(i, empty=_("Empty Slot."))
                    $ save_name = FileSaveName(i)

                    text "[file_name]. [file_time!t]\n[save_name!t]"

                    key "save_delete" action FileDelete(i)


screen save:

    # This ensures that any other menu screen is replaced.
    tag menu

    use navigation
    use file_picker

screen load:

    # This ensures that any other menu screen is replaced.
    tag menu

    use navigation
    use file_picker

init -2:
    style file_picker_frame is menu_frame
    style file_picker_nav_button is small_button
    style file_picker_nav_button_text is small_button_text
    style file_picker_button is large_button
    style file_picker_text is large_button_text


##############################################################################
# Preferences
#
# Screen that allows the user to change the preferences.
# http://www.renpy.org/doc/html/screen_special.html#prefereces

screen preferences:

    tag menu

    # Include the navigation.
    use navigation

    # Put the navigation columns in a three-wide grid.
    grid 3 1:
        style_group "prefs"
        xfill True

        # The left column.
        vbox:
            frame:
                style_group "pref"
                has vbox

                label _("Display")
                textbutton _("Window") action Preference("display", "window")
                textbutton _("Fullscreen") action Preference("display", "fullscreen")

            frame:
                style_group "pref"
                has vbox

                label _("Transitions")
                textbutton _("All") action Preference("transitions", "all")
                textbutton _("None") action Preference("transitions", "none")

            frame:
                style_group "pref"
                has vbox

                label _("Text Speed")
                bar value Preference("text speed")

            frame:
                style_group "pref"
                has vbox

                textbutton _("Joystick...") action Preference("joystick")


        vbox:
            frame:
                style_group "pref"
                has vbox

                label _("Skip")
                textbutton _("Seen Messages") action Preference("skip", "seen")
                textbutton _("All Messages") action Preference("skip", "all")

            frame:
                style_group "pref"
                has vbox

                textbutton _("Begin Skipping") action Skip()

            frame:
                style_group "pref"
                has vbox

                label _("After Choices")
                textbutton _("Stop Skipping") action Preference("after choices", "stop")
                textbutton _("Keep Skipping") action Preference("after choices", "skip")

            frame:
                style_group "pref"
                has vbox

                label _("Auto-Forward Time")
                bar value Preference("auto-forward time")

                if config.has_voice:
                    textbutton _("Wait for Voice") action Preference("wait for voice", "toggle")

        vbox:
            frame:
                style_group "pref"
                has vbox

                label _("Music Volume")
                bar value Preference("music volume")

            frame:
                style_group "pref"
                has vbox

                label _("Sound Volume")
                bar value Preference("sound volume")

                if config.sample_sound:
                    textbutton _("Test"):
                        action Play("sound", config.sample_sound)
                        style "soundtest_button"

            if config.has_voice:
                frame:
                    style_group "pref"
                    has vbox

                    label _("Voice Volume")
                    bar value Preference("voice volume")

                    textbutton _("Voice Sustain") action Preference("voice sustain", "toggle")
                    if config.sample_voice:
                        textbutton _("Test"):
                            action Play("voice", config.sample_voice)
                            style "soundtest_button"

init -2:
    style pref_frame:
        xfill True
        xmargin 5
        top_margin 5

    style pref_vbox:
        xfill True

    style pref_button:
        size_group "pref"
        xalign 1.0

    style pref_slider:
        xmaximum 192
        xalign 1.0

    style soundtest_button:
        xalign 1.0


##############################################################################
# Yes/No Prompt
#
# Screen that asks the user a yes or no question.
# http://www.renpy.org/doc/html/screen_special.html#yesno-prompt

screen yesno_prompt:

    modal True

    window:
        style "gm_root"

    frame:
        style_group "yesno"

        xfill True
        xmargin .05
        ypos .1
        yanchor 0
        ypadding .05

        has vbox:
            xalign .5
            yalign .5
            spacing 30

        label _(message):
            xalign 0.5

        hbox:
            xalign 0.5
            spacing 100

            textbutton _("Yes") action yes_action
            textbutton _("No") action no_action

    # Right-click and escape answer "no".
    key "game_menu" action no_action

init -2:
    style yesno_button:
        size_group "yesno"

    style yesno_label_text:
        text_align 0.5
        layout "subtitle"


##############################################################################
# Quick Menu
#
# A screen that's included by the default say screen, and adds quick access to
# several useful functions.
screen quick_menu:

    # Add an in-game quick menu.
    hbox:
        style_group "quick"

        xalign 1.0
        yalign 1.0

        textbutton _("Back") action Rollback()
        textbutton _("Save") action ShowMenu('save')
        textbutton _("Q.Save") action QuickSave()
        textbutton _("Q.Load") action QuickLoad()
        textbutton _("Skip") action Skip()
        textbutton _("F.Skip") action Skip(fast=True, confirm=True)
        textbutton _("Auto") action Preference("auto-forward", "toggle")
        textbutton _("Prefs") action ShowMenu('preferences')

init -2:
    style quick_button:
        is default
        background None
        xpadding 5

    style quick_button_text:
        is default
        size 12
        idle_color "#8888"
        hover_color "#ccc"
        selected_idle_color "#cc08"
        selected_hover_color "#cc0"
        insensitive_color "#4448"
            
##############################################################################
# Gallery by Rietr, v0.2
# For docs see http://www.renpy.org/doc/html/rooms.html

#we need to initialize some things for our gallery.

init python:
    ## DO NOT FORGET TO ADD 'textbutton _("Gallery") action ShowMenu("gallery")' TO SCREEN main_menu!
    # Create the gallery object , called 'gal'
    gal = Gallery()

    #Make sure that all the images defined in these settings exist
    ##### Settings: 
    # We need to declare all the images we want to include
    # Images should be defined under init python in script.rpy
    
    # Format of this list is as follows:
    # To simply create a gallery with one image behind each button fill the list with each image in a new list: [["example 1"],["example 2"]]
    # If you want to have multiple images behind one button do it like this: [["example 1","example 2"],["example 3"]].
    # In above list, example 1 and example 2 will be behind button 1 and example 3 will be on its own behind button 2
    # You can also put two images on top of each other, to combine character + background. 
    # This is done like this: [["example 1","example 2"],["example 3",["example 4","example 5"]]]
    # Now behind button 1 we have the images example 1 and example 2. Behind button two we first have example 3.
    # Then also behind button 2 we have example 5 on top of example 4.    
    
    # It is also possible to split it up, to create an easier overview. For the last example e.g.: [["example 1","example 2"]] + [["example 3",["example 4","example 5"]]]
    
    #!!!WARNING!!! (#this needs a fix somehow)
    #When including images A, B and C all behind a single button (in the order A,B,C)
    #make sure image A is unlocked before image B, and both are unlock before C, else this will result in a crash!
    
    imgs = [];
    
    # Images for the buttons (when unlocked) are defined below if you want this, fill it with images. First image for first button etc
    # If you do not like this leave the list empty and thumbnails will be automatically generated
    # Make sure you have as many buttons as that you have defined in imgs!
    butImgs = [];
    
    # Some options for structure. Changing number of cells also requires some tweaking for the thumbnail size.
    hor_cells = 3 #number of horizontal cells 
    ver_cells = 3 #number of vertical cells
    thumb_size_hor = 200 #thumbnail size (in pixels) in horizontal direction
    thumb_size_ver = 100 #thumbnail size (in pixels) in vertical direction    
    
    # Select background image
    bg_image = "galleryBG"
    # Select image for blocked galleries
    lockImg = "lockImg"
    # Select gallery transition, for possibilities: http://www.renpy.org/doc/html/transitions.html
    gal.transition = dissolve
    # Set the font size for text beneath buttons
    FontSize = 15
    
    ### Styling
    # Set position of the 'next page' button
    x_pos_next = 0.5
    y_pos_next = 0.95
    
    # Set position of the 'previous page' button
    x_pos_prev = 0.25
    y_pos_prev = 0.95
    
    # Set position of 'main menu'button
    x_pos_main = 0.95
    y_pos_main = 0.95
    
    # Set size of grid (in vertical direction)
    grid_size = 0.85
    
    # Move 'unlocked' text up or down
    text_ypos = 0.99
    ##### end of settings  

    # Now that all of the images have been included, we need to go over them all (looping) to add them to the gallery and create buttons
    for index, imgList in enumerate(imgs): #For each button the images are defined in a list
        gal.button(str(index) + "button")
        for item in imgList:
            if isinstance(item, basestring): #Normal occurence
                gal.unlock_image(item)
            else: #Combine images on top of each other
                gal.unlock_image(item[0], item[1])
                
    # Variable for setting the current page we ware one
    cur_page = 0
    no_cells = hor_cells*ver_cells
    max_page = (len(imgs)/(no_cells) - 1) + (float(len(imgs)) % (no_cells) > 0)


#All the button images need to be created after the initial init. 
init +10 python:
#    renpy.image("lockImgThumb", im.Scale(ImageReference(lockImg), thumb_size_hor, thumb_size_ver))
    for index, item in enumerate(imgs):
        if not butImgs:
            renpy.image(imgs[index][0] +"buttonImg", im.Scale(ImageReference(imgs[index][0]), thumb_size_hor, thumb_size_ver))
        else:
            renpy.image(butImgs[index]+"buttonImg", im.Scale(ImageReference(butImgs[index]), thumb_size_hor, thumb_size_ver))        

#that's that for now, now set up the screen
screen gallery:
    tag menu # Need this so program knows we are out of main menu
    add bg_image # Set the background
    grid hor_cells ver_cells: # Create the grid
        xfill True #Fill up the grids with background
        yfill True
        ysize grid_size
        $filled_cells = 0;
        # Add all of the buttons
        for index in range(cur_page*no_cells,min(cur_page*no_cells+no_cells,len(imgs))):
            if not butImgs:
                add gal.make_button(str(index)+"button", imgs[index][0] + "buttonImg", "lockImgThumb", xalign=0.5, yalign=0.5)
            else:
                add gal.make_button(str(index) + "button", butImgs[index]+ "buttonImg", "lockImgThumb", xalign=0.5, yalign=0.5)
            $filled_cells +=1
        for fill in range(filled_cells, no_cells): #fill up all the remaining cells
            null
    grid hor_cells ver_cells:
        xfill True
        yfill True
        ysize grid_size
        $filled_cells = 0;
        for index in range(cur_page*no_cells, min(cur_page*no_cells+no_cells,len(imgs))):
            text "Images unlocked of total: "+ gal.get_fraction(str(index)+"button",format='{seen}/{total}') xalign 0.5 yalign text_ypos size FontSize
            $filled_cells +=1 #for each cell add to this            
        for fill in range(filled_cells, no_cells): #fill up all the remaining cells
            null        
    #Main menu button
    frame: 
        xalign x_pos_main
        yalign y_pos_main        
        vbox:
            textbutton _("Main menu") action Return()
    #Next page button        
    if cur_page < max_page:
        frame:
            xalign x_pos_next
            yalign y_pos_next
            vbox:
                textbutton _("Next") action [SetVariable('cur_page', cur_page +1), ShowMenu("gallery")]
    #Previous page button
    if cur_page > 0:
        frame:
            xalign x_pos_prev
            yalign y_pos_prev
            vbox:
                textbutton _("Previous") action [SetVariable('cur_page', cur_page - 1), ShowMenu("gallery")]
        

##############################################################################
# Music room by Rietr, v0.1alpha
# For docs see http://www.renpy.org/doc/html/rooms.html

#Set the folder containing all the tracks you want to load

# Initialize our music room 
init -10 python:
    paused = False

init python:
    music_folder = 'music'

    theMusicRoom = MusicRoom(fadeout=1.0)
    #Adding all the songs ##(seriously, there has to be some better way?)
    tracks = load_tracks(music_folder)
    for track in tracks:
        theMusicRoom.add(music_folder + "/" + track, always_unlocked = True)  
    paused = False
    
    def pauseReset():
        global paused
        paused = False
        renpy.audio.audio.pss.unpause(7)



screen music_room:
    tag menu
    frame:
        xalign 0.5
        yalign 0.5
        vbox:
        # The buttons that play each track.
            python:
                for track in tracks:
                    ui.textbutton(os.path.splitext(track)[0], clicked = [theMusicRoom.Play(music_folder + "/" + track),pauseReset])
        #null height 20
    frame:
        xalign 0.8
        yalign 0.8
        hbox:
        # Buttons that let us advance tracks.
            textbutton "Previous" action theMusicRoom.Previous()
            textbutton "Pause" action pauseSwitch
            textbutton "Stop" action theMusicRoom.Stop()           
            textbutton "Next" action theMusicRoom.Next()

        #null height 20
        
    frame:
        xalign 0.9
        yalign 0.9
        # The button that lets the user exit the music room.
        textbutton "Main Menu" action ShowMenu("main_menu") 

    # Start the music playing on entry to the music room.
    #on "replace" action theMusicRoom.Play()

    # Restore the main menu music upon leaving.
    on "replaced" action theMusicRoom.Stop()
    