import os
import sys
from pathlib import Path
cwd = os.getcwd()

file_path = f'{Path(cwd).parent.parent}\Log'

print(file_path)


