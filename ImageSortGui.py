#http://appjar.info/ tuolta löytyy appjar dokumentaatiota
import threading
import sys
import os
# Find path for Scripts folder
sys.path.append(os.path.abspath('Scripts'))
import classify_image
import tkinter as tk
from subprocess import call
from appJar import gui
from tkinter.filedialog import askdirectory


filters={"Dog":False, "Cat":False, "Bacon":False,
            "Lakeside":False, "Fire":False}

#This define should print the image directory --so that it could be called in the loop. 
def pressGo(btn):
    print("ass")


app = gui()

app.setSize(400, 600)
app.addLabel("l1", "Choose a folder")
app.addDirectoryEntry("d1")
app.addLabel("l2", "Choose folder for filtered images")
app.addDirectoryEntry("d2")
app.addProperties("Choose Filters", filters )
app.addButton("Go", pressGo)

app.go()
