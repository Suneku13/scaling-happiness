init python:
    import os
    def load_tracks(directory):
        tracks = []
        for dirName, subdirList, fileList in os.walk(config.gamedir + "/" + directory):
            for file in fileList:
                extension = os.path.splitext(file)[1].lower()
                if extension == ".mp3" or extension == ".ogg" or extension == ".wav":
                    tracks.append(file)
        return tracks