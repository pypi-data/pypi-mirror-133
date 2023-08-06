import os
import pathlib

ipynb_path = pathlib.Path(__file__).parent.resolve() + '/frontend.ipynb'
os.system('voila ' + ipynb_path)
