import sys
from cx_Freeze import setup, Executable

executables = [Executable('main.py')]

build_options = {
    'build_exe': {
        'packages': ['random'],
        'excludes': [],
        'include_files': []
    }
}
  
setup(
    name='Batalha pela República',
    version='1.0',
    description='Em Batalha Pela República, o jogador toma o lugar de D. Pedro II para evitar que a república seja proclamada no Brasil',
    options=build_options,
    executables=executables
)