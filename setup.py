from cx_Freeze import setup, Executable
import os

os.environ['TCL_LIBRARY'] = r'C:/Users/cxn/AppData/Local/Programs/Python/Python35/tcl/tcl8.6'
os.environ['TK_LIBRARY'] = r'C:/Users/cxn/AppData/Local/Programs/Python/Python35/tcl/tk8.6'

base = None    

executables = [Executable("D:/development/test-code/test/requests-test.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "test",
    options = options,
    version = "1.0",
    description = 'any description',
    executables = executables
)