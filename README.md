# Interleaving Simulator Application using Python tkinter
![Thumbnail1](assets/thumbnail1.jpg)

![Thumbnail2](assets/thumbnail2.jpg)


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
pip install auto-py-to-exe
```


## How to compile `.py` to `.exe` file (pyinstaller)
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
