import shutil
import sys
sys.path.append(os.path.abspath('Scripts'))
import classify_image
import os


def SelectFilters(sourceFolder, targetFolder, filters):
    #store selected filters as strings for later use (selectedTags)
    _filters = filters
    _sourceFolder = sourceFolder
    _targetFolder = targetFolder
    
    for _file in _sourceFolder:
    #loops through the file(s) in a given folderpath, 
    
        if _file.lower().endswith(('.png', '.jpg', '.jpeg')):
            #sends FILEPATH to  classify function and receives tagString containing 5 highest tags and their variables
            _filePath = _sourceFolder + '\\' + _file
            _tagString = str(classify_image.ClassifyImage(_filePath))
        
            if _filter in _tagString:
            #change the filepath/folder to corresponding tagfolder, also checks if one exists or not and creates one if
            #neccesary.
                   
                #newpath = r'C:\Program Files\arbitrary'#!!!!swap the directory for this code!!! 
                if not os.path.exists(_targetFolder): #if the dir doesn't exist
                    os.makedirs(_targetFolder)#this creates it
                        
                shutil.move(src, dst, copy_function=copy2)
                #Recursively move a file or directory (src) to another location (dst) and return the destination.
                    
            else:
                pass #if no tags found in tagString, do nothing.
        else:
            pass #do nothing if the file isnt an image file