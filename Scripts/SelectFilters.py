import shutil
import sys
import os
sys.path.append(os.path.abspath('Scripts'))
import classify_image



def SelectFilters(sourceFolder, targetFolder, filters):
    #store selected filters as strings for later use (selectedTags)
    _filters = filters
    _sourceFolder = sourceFolder
    _targetFolder = targetFolder
    print('Start Program')
    
    for _file in os.listdir(_sourceFolder):
    #loops through the file(s) in a given folderpath,
        print('Reading File')
        if _file.endswith(('.png', '.jpg', '.jpeg')):
            print('Image File Found')
            #sends FILEPATH to  classify function and receives tagString containing 5 highest tags and their variables
            _imagePath = _sourceFolder + '\\' + _file
            print('Classifying Image...')
            _match = classify_image.ClassifyImage(_imagePath, _filters)
            print('...Done! Result: ' + str(_match))
            if _match is True:
                print('Filter Match with: ' + _imagePath)
            #change the filepath/folder to corresponding tagfolder, also checks if one exists or not and creates one if
            #neccesary.
                print('Check for Folders')
                if not os.path.exists(_targetFolder): #if the dir doesn't exist
                    os.makedirs(_targetFolder)#this creates it
                    
                _filters = _filters.capitalize()    
                if not os.path.exists(_targetFolder + '\\' + _filters + ' Pictures'): #Same as above for filtered folder
                    os.makedirs(_targetFolder + '\\' + _filters + ' Pictures')
                print('Moving File...')
                    
                shutil.move(_imagePath, _targetFolder + '\\' + _filters + ' Pictures\\' + _file)
                #Recursively move a file or directory (src) to another location (dst) and return the destination.
                _filters = _filters.lower()
                print('...Done!')
                    
            else:
                pass #if no tags found in tagString, do nothing.
        else:
            pass #do nothing if the file isnt an image file
# Test functionality       
#SelectFilters('C:\\Users\\admin\\Desktop\\test\\Source', 'C:\\Users\\admin\\Desktop\\test\\Dest', 'animal')