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
    
    for _file in os.listdir(_sourceFolder):
    #loops through the file(s) in a given folderpath, 
        if _file.lower().endswith(('.png', '.jpg', '.jpeg')):
            #sends FILEPATH to  classify function and receives tagString containing 5 highest tags and their variables
            _imagePath = _sourceFolder + '\\' + _file
            _tagString = str(classify_image.ClassifyImage(_imagePath))
            if _filters in _tagString:
                print(_filters, _tagString)
            #change the filepath/folder to corresponding tagfolder, also checks if one exists or not and creates one if
            #neccesary.
                   
                if not os.path.exists(_targetFolder): #if the dir doesn't exist
                    os.makedirs(_targetFolder)#this creates it
                        
                shutil.move(_imagePath, _targetFolder + '\\' + _file)
                #Recursively move a file or directory (src) to another location (dst) and return the destination.
                    
            else:
                pass #if no tags found in tagString, do nothing.
        else:
            pass #do nothing if the file isnt an image file
# Test functionality       
#SelectFilters('C:\\Users\\admin\\Desktop\\test\\Source', 'C:\\Users\\admin\\Desktop\\test\\Dest', 'vulture')