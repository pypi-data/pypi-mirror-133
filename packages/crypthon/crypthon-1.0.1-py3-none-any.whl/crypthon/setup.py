from cx_Freeze import setup, Executable

base = None    

executables = [Executable("crypthon.py", base=base)]

packages = ["idna", "os", "sys", "obfus"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "crypthon",
    options = options,
    version = "1.0",
    description = 'software by Gilda',
    executables = executables
)