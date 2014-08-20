init python:
    def pauseSwitch():
        global paused
        if not paused and renpy.music.get_playing():
            renpy.audio.audio.pss.pause(7)
            paused = True
        else:
            renpy.audio.audio.pss.unpause(7)
            paused = False

            