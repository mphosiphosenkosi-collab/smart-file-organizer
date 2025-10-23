"""
SMART FILE ORGANIZER
Copyright (c) 2024 J. Siphosenkosi Sibiya

This software is licensed under the MIT License.
See LICENSE file for details.
"""



import os
import shutil
import argparse
import logging
from datetime import datetime
import csv
import pandas as pd 

# -------------------------------
# Logging Setup 
# -------------------------------
os.makedirs("logs", exist_ok=True)
log_file = f"logs/organizer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------------------
# File Type Categories
# -------------------------------
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"],
    "Videos": [".mp4", ".avi", ".mov", ".mkv"],
    "Music": [".mp3", ".wav", ".flac"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Others": []
}

# Month names with numbers
MONTHS = [
    "01_January", "02_February", "03_March", "04_April",
    "05_May", "06_June", "07_July", "08_August",
    "09_September", "10_October", "11_November", "12_December"
]

# -------------------------------
# Global list to collect report data
# -------------------------------
file_report = []

# -------------------------------
# Helper Functions
# -------------------------------
def get_file_category(filename):
    """Determine the category of a file based on its extension."""
    for category, extensions in FILE_TYPES.items():
        if filename.lower().endswith(tuple(extensions)):
            return category
    return "Others"

def get_year_month_folder(file_path, base_folder):
    """Return the target folder path for the file based on its date and category."""
    timestamp = os.path.getmtime(file_path)
    file_date = datetime.fromtimestamp(timestamp)
    year = str(file_date.year)
    month_folder = MONTHS[file_date.month - 1]  

    category = get_file_category(file_path)
    folder_path = os.path.join(base_folder, category, year, month_folder)
    return folder_path

def move_file(file_path, base_folder, dry_run=False):
    """Move a file and record info for reporting."""
    target_folder = get_year_month_folder(file_path, base_folder)
    os.makedirs(target_folder, exist_ok=True)
    destination = os.path.join(target_folder, os.path.basename(file_path))

    category = get_file_category(file_path)
    timestamp = os.path.getmtime(file_path)
    file_date = datetime.fromtimestamp(timestamp)
    year = str(file_date.year)
    month = MONTHS[file_date.month - 1]

    # Record file info for CSV report
    file_report.append({
        "File Name": os.path.basename(file_path),
        "Original Path": file_path,
        "Category": category,
        "Year": year,
        "Month": month,
        "Target Path": destination
    })

    if os.path.exists(destination):
        logging.warning(f"Duplicate found, skipping: {file_path}")
        print(f"Duplicate found, skipping: {file_path}")
        return

    if dry_run:
        logging.info(f"[DRY RUN] Would move {file_path} -> {destination}")
        print(f"[DRY RUN] Would move {file_path} -> {destination}")
    else:
        shutil.move(file_path, destination)
        logging.info(f"Moved {file_path} -> {destination}")
        print(f"Moved {file_path} -> {destination}")

def save_report_csv(filename="file_report.xlsx"):
    """Save collected file info in a structured table (Excel format) - FIXED LOCATION"""
    if not file_report:
        print("No files to report.")
        return
    
    reports_folder = os.path.join(os.getcwd(), "reports")
    if not os.path.exists(reports_folder):
        os.makedirs(reports_folder)

    df = pd.DataFrame(file_report) 

    # sort for readability
    df = df.sort_values(by=["Category", "Year", "Month", "File Name"])

    # Save as Excel with proper table format - FIXED: save in reports folder
    file_path = os.path.join(reports_folder, filename)
    df.to_excel(file_path, index=False)
    print(f"Structured report saved: {file_path}")
    logging.info(f"Report saved: {file_path}")

def organize_files(source_folder, dry_run=False):
    """Organize all files in the source folder dynamically by category/year/month."""
    if not os.path.exists(source_folder):
        print(f"Source folder does not exist: {source_folder}")
        return

    files_moved = False
    
    # RECURSIVE SEARCH
    for root, dirs, files in os.walk(source_folder):
        for filename in files:
            file_path = os.path.join(root, filename)
            
          
            if not os.path.isfile(file_path):
                continue
                
            if root != source_folder and any(part in FILE_TYPES.keys() for part in root.split(os.sep)):
                continue
                
            move_file(file_path, source_folder, dry_run=dry_run)
            files_moved = True
            
    save_report_csv()  
    
    if files_moved:
        print("File organization complete!")
        print(f"📊 Logs saved in: {log_file}")
       
    else:
        print("No files found to organize.")

# -------------------------------
# Reset Folder Function
# -------------------------------
def reset_folder(folder_path):
    """Delete all files and subfolders in the target folder."""
    if not os.path.exists(folder_path):
        print(f"Folder does not exist: {folder_path}")
        return
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
    print(f"All files and subfolders in '{folder_path}' have been deleted!")
    logging.info(f"Reset folder: {folder_path}")

# -------------------------------
# Command-Line Interface
# -------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Smart File Organizer with CSV Reporting")
    parser.add_argument("source_folder", help="Path to the folder to organize")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without moving files")
    parser.add_argument("--reset", action="store_true", help="Delete all files and subfolders in the folder")
    args = parser.parse_args()

    if args.reset:
        reset_folder(args.source_folder)
    else:
        organize_files(args.source_folder, dry_run=args.dry_run)


