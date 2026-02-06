import os
import sys

def initialize_project():
    
    folders = ['models', 'data', 'logs', 'modules', 'core', 'scripts']
    
    print(" Initializing CropVanta.AI Environment...")
    
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f" Created folder: {folder}")
        else:
            print(f" Folder already exists: {folder}")

    log_file = "logs/app.log"
    if not os.path.exists(log_file):
        with open(log_file, "w") as f:
            f.write("--- Log Initialized ---")
        print(f"Created file: {log_file}")

if __name__ == "__main__":
    initialize_project()