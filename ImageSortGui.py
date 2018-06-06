#http://appjar.info/ tuolta löytyy appjar dokumentaatiota
import threading
import sys
import os

# Find path for Scripts folder
sys.path.append(os.path.abspath('Scripts'))

import SelectFilters
from subprocess import call
from appJar import gui

filters={"Dog":False, "Cat":False, "Food":False,
         "Building":False, "Animal":False, "Pet":False,
         "Scenery":False}



#This define prints the image directory --so that it could be called in the imagesortingloop.
def pressGo(btn):        
    # Next loop only enables one filter
    _oneFilter = ''
    _filters = app.getProperties("Choose Filters")
    for k, v in _filters.items():
        if v is True:
            _oneFilter = k
            _oneFilter = _oneFilter.lower()
            print(_oneFilter)

    _source = app.getEntry("d1")
    _dest = app.getEntry("d2")
    if _source is not None and _dest is not None and _oneFilter is not None:
        #SelectFilters.SelectFilters(_source, _dest, _oneFilter)
        app.thread(SelectFilters.SelectFilters, _source, _dest, _oneFilter)


app = gui()


app.addLabel("l1", "Choose a folder")
app.addDirectoryEntry("d1")
app.addLabel("l2", "Choose folder for filtered images")
app.addDirectoryEntry("d2")
app.addProperties("Choose Filters", filters )
app.addButton("Go", pressGo)


app.setSize(400, 600)


app.go()

