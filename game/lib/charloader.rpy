init python:
    import os
    #this function will automatically add all characters
    def load_chars():
        for char, props in characters.iteritems():
            if 'two' in props:
                twowindow = props['two']
            else: 
                twowindow = False
            if 'kind' in props:
                globals()[props['short']] = Character(char,color=props['color'],show_two_window=twowindow,kind=props['kind'])
            else:
                globals()[props['short']] = Character(char,color=props['color'],show_two_window=twowindow)
