init python:
    import os
    # This function will automatically load all images in the folder given and will add a prefix if given, otherwise no prefix is added
    def load_images(folder, prefix=""):
        base=config.gamedir
        for dirName, subdirList, fileList in os.walk(base+"/"+folder):
            subdir = dirName.split(folder)[-1]
            subdirName = subdir.split('/')
            for fileName in fileList:
                renpy.image((prefix+ ' '.join(subdirName) + ' ' + os.path.splitext(fileName)[0]).lower(),folder+subdir+'/'+fileName)