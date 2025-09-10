SMART FILE ORGANIZER

A powerful Python-based file organization tool with SHA256 deduplication, Excel reporting, and safety backups.

## Features

- **Content-based categorization**: Organize files by type, year, and month
- **SHA256 deduplication**: Eliminate duplicate files using cryptographic hashing
- **Excel reports**: Comprehensive reporting with category sheets and summaries
- **Safety-mode backups**: Automatic restore points before organizing
- **Parallel processing**: Multi-threaded file operations for improved performance
- **Logging**: Detailed execution logs with timestamps

## Installation

1. Clone or download this repository
2. Install required dependencies:
pip install -r requirements.txt



## Usage

### Basic File Organization
python organizer.py <source_folder>
python organizer.py <source_folder> --dry-run
python organizer.py <source_folder> --safety-mode
python organizer.py <source_folder> --workers 8
python organizer.py <source_folder> --no-duplicates



### Folder & File Maintenance
python organizer.py <source_folder> --reset
python organizer.py <source_folder> --clean-logs 7
python organizer.py <source_folder> --clean-reports 30



### Restore/Backup Management
python organizer.py <source_folder> --list-restores
python organizer.py <source_folder> --restore-last



## Command Cheat Sheet

### 1️⃣ Basic File Organization
python organizer.py <source_folder> Organize all files in folder into category/year/month.
python organizer.py <source_folder> --dry-run Simulate organization without moving files.
python organizer.py <source_folder> --safety-mode Create backup restore point before organizing.
python organizer.py <source_folder> --workers 8 Use 8 parallel threads (adjust number as needed).
python organizer.py <source_folder> --no-duplicates Skip duplicate handling (don't move duplicates).
python organizer.py <source_folder> --dry-run --safety-mode --workers 6 Combine multiple options.



### 2️⃣ Folder & File Maintenance
python organizer.py <source_folder> --reset Delete all files and subfolders (folder remains).
python organizer.py <source_folder> --clean-logs 7 Delete log files older than 7 days (default 7).
python organizer.py <source_folder> --clean-reports 30 Delete reports older than 30 days (default 30).



### 3️⃣ Restore / Backup Management
python organizer.py <source_folder> --list-restores List all available restore points.
python organizer.py <source_folder> --restore-last Restore the folder from the latest backup.



Note: Restore points are stored in restore_points/ folder as timestamped zip files.

### 4️⃣ Reports & Logs
reports/ Excel/CSV reports per category, duplicates, summary.
logs/ Script execution logs with timestamps.



Example:
Open latest log
notepad logs/organizer_20250909_150102.log

Open latest report
open reports/file_report_20250909_150102.xlsx



## Example Workflow

1. Simulate organization first:
python organizer.py test_files --dry-run --safety-mode



2. Organize files with 6 threads:
python organizer.py test_files --workers 6 --safety-mode



3. Clean old logs and reports:
python organizer.py test_files --clean-logs 7
python organizer.py test_files --clean-reports 30



4. Restore folder if needed:
python organizer.py test_files --restore-last



5. Reset folder for fresh start:
python organizer.py test_files --reset



## Tips & Best Practices

- Always start with --dry-run for new folders.
- Use --safety-mode for critical files to ensure a backup exists.
- DUPLICATES folder is created at the top level of your source folder.
- Multi-sheet Excel report gives full overview:
  - Category sheets
  - Duplicates sheets
  - Summary sheet
- Logs are timestamped: helpful for troubleshooting.
- Files already inside category folders are skipped automatically.

## Project Structure

The script automatically creates these directories:
- `logs/`: Execution logs with timestamps
- `reports/`: Excel reports with file details
- `restore_points/`: Backup zip files
- `DUPLICATES/`: Files identified as duplicates

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
