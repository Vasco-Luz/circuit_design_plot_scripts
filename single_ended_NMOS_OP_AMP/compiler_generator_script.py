import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # Add import statement for NumPy
import subprocess
import time


script_dir = os.path.dirname(__file__)

subprocess.run(['python3', os.path.join(script_dir,'bias_nmos.py')])

subprocess.run(['python3', os.path.join(script_dir,'bias_nmos_mc.py')])

subprocess.run(['python3', os.path.join(script_dir,'PMOS_load_characterisation.py')])

subprocess.run(['pdflatex', os.path.join(script_dir,'NMOS_opamp_cell_atuomatic_documentation.tex')])