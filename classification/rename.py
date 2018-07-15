import os
import glob
for file in glob.glob("voice2"):
    newfile = str(i)+ "-2.wav"
    os.rename(file, newfile)