
import os

# Set the directory you want to start from
rootDir = '/home/martin/GISfun'
for dirName, subdirList, fileList in os.walk(rootDir):
    print('Found directory: %s' % dirName)
    if len(fileList) > 0:
        for fname in fileList:
            print(' --> %s' % fname)
    else:
        print " --- No files here..."