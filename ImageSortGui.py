#http://appjar.info/ 
import threading
import sys
import os

# Find path for Scripts folder
sys.path.append(os.path.abspath('Scripts'))

import SelectFilters
from appJar import gui

filters={"Dog":False, "Cat":False, "Food":False,
         "Building":False, "Animal":False, "Pet":False,
         "Scenery":False}

def pressGo(btn):        
    # Next loop only enables one filter
    _oneFilter = ''
    _filters = app.getProperties("Choose Filters")
    # k (key) means here the filter like 'dog'
    # v (value) is the boolean value. If the box is selected = True
    for k, v in _filters.items():  
        if v is True:
            _oneFilter = k
            # At the moment classifyImage is case sensitive:
            _oneFilter = _oneFilter.lower()

    _source = app.getEntry("d1")
    _dest = app.getEntry("d2")
    if _source is not None and _dest is not None and _oneFilter is not None:
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

