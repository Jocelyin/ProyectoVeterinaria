import os
import sys
print(f"CWD: {os.getcwd()}")
print(f"Sys Path: {sys.path}")
try:
    import api
    print(f"API File: {api.__file__}")
    from api import app
    print(f"App Title: {app.title}")
except ImportError as e:
    print(f"Import Error: {e}")
except Exception as e:
    print(f"Error: {e}")
