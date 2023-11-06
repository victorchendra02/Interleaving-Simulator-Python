## How to run without Python
Simply open `dist` folder, and open `Interleaving Simulator.exe` file


## Activate Python virtual environement
```bash
venv\Scripts\activate
```


## Python library requirement
```bash
pip install tkinter
pip install pyinstaller
```


## How to compile `.py` to `.exe` file
```bash
# Compile normal
pyinstaller main.py

# Compile with no terminal
pyinstaller main.py --windowed

# Compile into single file and no terminal
pyinstaller main.py --onefile --windowed

# Compile into single file, no terminal, and set icon app
pyinstaller main.py --onefile --windowed --icon="assets\interleaving app.ico"

# Compile into single file, no terminal, set icon app, and set name for the app after compiled
pyinstaller main.py --onefile --windowed --icon="assets\interleaving app.ico" --name="Interleaving Simulator"
```
