#!/usr/bin/env python3
"""
Build script to create a standalone executable for the Flask backend using PyInstaller.
This ensures the backend can run without requiring Python installation.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_backend():
    """Build the backend into a standalone executable."""
    
    # Get the directory containing this script
    backend_dir = Path(__file__).parent
    
    # Paths
    app_py = backend_dir / "app.py"
    dist_dir = backend_dir / "dist"
    build_dir = backend_dir / "build"
    
    # PyInstaller command
    pyinstaller_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",  # Create a single executable
        "--name", "horary_backend",
        "--distpath", str(dist_dir),
        "--workpath", str(build_dir),
        "--specpath", str(backend_dir),
        # Include data files
        "--add-data", f"{backend_dir / 'horary_constants.yaml'};.",
        "--add-data", f"{backend_dir / 'horary_config.py'};.",
        "--add-data", f"{backend_dir / 'production_server.py'};.",
        # Hidden imports for modules that PyInstaller might miss
        "--hidden-import", "swisseph",
        "--hidden-import", "timezonefinder",
        "--hidden-import", "geopy",
        "--hidden-import", "pytz",
        "--hidden-import", "flask",
        "--hidden-import", "flask_cors",
        # Console application (not windowed)
        "--console",
        # Don't create __pycache__ folders
        "--clean",
        str(app_py)
    ]
    
    print("Building backend executable...")
    print(f"Command: {' '.join(pyinstaller_cmd)}")
    
    try:
        # Clean previous builds
        if dist_dir.exists():
            shutil.rmtree(dist_dir)
        if build_dir.exists():
            shutil.rmtree(build_dir)
            
        # Run PyInstaller
        result = subprocess.run(pyinstaller_cmd, check=True, cwd=backend_dir)
        
        if result.returncode == 0:
            exe_path = dist_dir / "horary_backend.exe" if sys.platform == "win32" else dist_dir / "horary_backend"
            if exe_path.exists():
                print(f"✓ Backend executable created: {exe_path}")
                print(f"✓ Size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
                return str(exe_path)
            else:
                print("✗ Executable not found after build")
                return None
        else:
            print("✗ PyInstaller failed")
            return None
            
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        return None
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return None

if __name__ == "__main__":
    exe_path = build_backend()
    if exe_path:
        print("\nTo test the executable:")
        print(f"  {exe_path}")
        print("\nThe executable should be copied to the Electron app's resources folder.")
    else:
        sys.exit(1)