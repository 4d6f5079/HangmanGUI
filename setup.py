import cx_Freeze
import os.path

executables = [cx_Freeze.Executable("HangManGame.py")]
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

cx_Freeze.setup(
    name = "Hangman",
    options={"build_exe": {"packages": ["pygame"],
                           'include_files': [
                               os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
                               os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
                           ]
                           }},
    executables = executables )