import os
import glob
i = 0
for file in glob.glob("*.wav"):
    newfile = str(i)+ "-2.wav"
    os.rename(file, newfile)
    i+=1