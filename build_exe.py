import PyInstaller.__main__
import os
import sys

def build():
    # Define the entry point
    entry_point = os.path.join("skelter", "cli", "main.py")
    
    # PyInstaller arguments
    args = [
        entry_point,
        "--onefile",
        "--name=skelter",
        "--clean",
        # Use logo as icon (Windows handles PNG conversion in newer PyInstaller)
        "--icon=logo_2.png",
        # Bundle the logo as a data file
        "--add-data=logo_2.png;.",
        # Include the skelter package
        "--collect-all=skelter",
        # Explicitly include dependencies that might be missed
        "--hidden-import=uvicorn.logging",
        "--hidden-import=uvicorn.loops",
        "--hidden-import=uvicorn.loops.auto",
        "--hidden-import=uvicorn.protocols",
        "--hidden-import=uvicorn.protocols.http",
        "--hidden-import=uvicorn.protocols.http.auto",
        "--hidden-import=uvicorn.protocols.websockets",
        "--hidden-import=uvicorn.protocols.websockets.auto",
        "--hidden-import=uvicorn.lifespan",
        "--hidden-import=uvicorn.lifespan.on",
    ]
    
    PyInstaller.__main__.run(args)

if __name__ == "__main__":
    build()
