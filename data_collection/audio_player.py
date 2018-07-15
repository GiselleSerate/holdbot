import os
import subprocess

_BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
_FILE_DIR = os.path.join(_BASE, 'hold_audio')

def play_audio():
    for filename in os.listdir(_FILE_DIR):
        print(filename)
        subprocess.call('afplay {0}'.format(os.path.join(_FILE_DIR, filename)), shell=True)
