import os
import sys

def initialize_project():
    """
    Creates necessary directories and placeholder files 
    to ensure the app doesn't crash on the first run.
    """
    # Essential folders for the production-grade architecture
    folders = ['models', 'data', 'logs', 'modules', 'core', 'scripts']
    
    print("🚀 Initializing CropVanta.AI Environment...")
    
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"✅ Created folder: {folder}")
        else:
            print(f"ℹ️ Folder already exists: {folder}")

    # Create a blank log file to avoid 'File Not Found' errors
    log_file = "logs/app.log"
    if not os.path.exists(log_file):
        with open(log_file, "w") as f:
            f.write("--- Log Initialized ---")
        print(f"✅ Created file: {log_file}")

if __name__ == "__main__":
    initialize_project()