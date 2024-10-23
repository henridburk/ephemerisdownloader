import requests
import os
import argparse
import logging
import gzip
import shutil
import time
from datetime import datetime, timedelta
from logging.handlers import TimedRotatingFileHandler

# Default directory for downloading ephemeris files
DEFAULT_DOWNLOAD_DIR = "downloads"

# Base URL for downloading the ephemeris files (with dynamic year)
def get_base_url():
    """Return the base URL with the current year."""
    current_year = datetime.now().year
    return f"https://cddis.nasa.gov/archive/gnss/data/daily/{current_year}/brdc/"

# Ensure the logs directory exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Define log filename with the current date
log_filename = os.path.join(LOG_DIR, f"ephemeris_downloader_{datetime.now().strftime('%Y-%m-%d')}.log")

# Setup logging with daily rotation and retention for 7 days
log_handler = TimedRotatingFileHandler(
    log_filename, when="midnight", interval=1, backupCount=7
)
log_handler.setLevel(logging.INFO)
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        log_handler,
        logging.StreamHandler()
    ]
)

def get_day_of_year(offset=0, specific_date=None):
    """Return the day of the year with an optional offset or a specific date."""
    if specific_date:
        specific_date_dt = datetime.strptime(specific_date, "%d-%m-%Y")
        day_of_year = specific_date_dt.timetuple().tm_yday
    else:
        now = datetime.now() - timedelta(days=offset)
        day_of_year = now.timetuple().tm_yday
    return day_of_year

def construct_filename(day_of_year):
    """Construct the ephemeris filename based on the day of the year and current year."""
    current_year = datetime.now().year
    year_suffix = str(current_year)[-2:]  # Last two digits of the current year
    filename = f"brdc{day_of_year:03d}0.{year_suffix}n.gz"  # Use .{year_suffix}n.gz format
    return filename

def download_ephemeris_file(day_of_year, download_dir, retries=0, wait_minutes=0):
    """Download the ephemeris file for a given day of the year and directory."""
    filename = construct_filename(day_of_year)
    file_url = get_base_url() + filename  # Use dynamic URL based on the year
    local_file_path = os.path.join(download_dir, filename)

    # Create the download directory if it doesn't exist
    os.makedirs(download_dir, exist_ok=True)

    attempt = 1
    while attempt <= retries + 1:  # +1 for the initial attempt
        logging.info(f"Attempt {attempt}: Starting download for {filename} from {file_url}")

        try:
            # Make the request
            response = requests.get(file_url)

            # Check if the request was successful
            if response.status_code == 200:
                with open(local_file_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=1000):
                        file.write(chunk)
                logging.info(f"File {filename} downloaded successfully to {local_file_path}")

                # Unzip the file after download
                unzip_file(local_file_path)
                break  # Exit the loop on success

            elif response.status_code == 404:
                logging.error(f"File not found: {filename}. Status code: {response.status_code}")
                # If it's a 404 error, log it but don't break the loop.

            else:
                logging.error(f"Failed to download file {filename}. Status code: {response.status_code}")

        except requests.exceptions.ConnectionError as e:
            logging.error(f"Connection error occurred: {str(e)}")
        
        except Exception as e:
            logging.error(f"An error occurred while downloading {filename}: {str(e)}")

        if attempt < retries + 1:  # If it's not the last attempt
            wait_time = wait_minutes * 60  # Convert to seconds
            logging.info(f"Retrying in {wait_minutes} minutes...")
            time.sleep(wait_time)

        attempt += 1

    if attempt > retries + 1:  # If all attempts failed
        logging.error(f"All retry attempts failed for {filename}.")

def unzip_file(file_path):
    """Unzip the .gz file."""
    try:
        with gzip.open(file_path, 'rb') as f_in:
            output_file_path = file_path[:-3]  # Remove the .gz extension
            with open(output_file_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        logging.info(f"File {file_path} unzipped successfully to {output_file_path}")

        # Optionally, delete the .gz file after extraction
        os.remove(file_path)
        logging.info(f"Deleted the original gz file: {file_path}")
    except Exception as e:
        logging.error(f"Failed to unzip file {file_path}. Error: {str(e)}")

def download_batch_files(last_days, download_dir, retries=0, wait_minutes=0):
    """Download ephemeris files for the last X days."""
    for offset in range(last_days):
        download_ephemeris_file(get_day_of_year(offset), download_dir, retries, wait_minutes)

def delete_file(offset=None, specific_date=None, download_dir=DEFAULT_DOWNLOAD_DIR):
    """Delete the file for the given offset or specific date."""
    if specific_date:
        day_of_year = get_day_of_year(specific_date=specific_date)
    else:
        day_of_year = get_day_of_year(offset=offset)
    
    filename = construct_filename(day_of_year)
    file_path = os.path.join(download_dir, filename[:-3])  # Removing the .gz extension

    if os.path.isfile(file_path):
        os.remove(file_path)
        logging.info(f"Deleted file: {file_path}")
    else:
        logging.warning(f"No file found to delete for {filename[:-3]} in {download_dir}.")

def delete_batch_files(last_days, download_dir):
    """Delete ephemeris files for the last X days."""
    for offset in range(last_days):
        delete_file(offset=offset, download_dir=download_dir)

def main():
    # Argument parser setup
    parser = argparse.ArgumentParser(
        description='Download and manage ephemeris files from NASA.',
        epilog='''\
Functionality:
This script allows you to download GNSS ephemeris files from NASA's CDDIS archive.
You can download specific files based on the current date, past dates, or batch download
files for a specified number of days. You can also delete specific files as needed.
''',
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument('-o', '--offset', type=int, default=0,
                        help='Offset in days from today (0 for today, 1 for yesterday, etc.)')
    parser.add_argument('-d', '--delete', action='store_true',
                        help='Delete the file for the given offset or specific date.')
    parser.add_argument('-s', '--specific_date', type=str,
                        help='Specific date in dd-mm-yyyy format for download or delete.')
    parser.add_argument('-l', '--last_days', type=int,
                        help='Download or delete files for the last X days.')
    parser.add_argument('-dir', '--directory', type=str, default=DEFAULT_DOWNLOAD_DIR,
                        help='Directory where the ephemeris files will be downloaded or deleted.')
    parser.add_argument('-r', '--retry', type=int, nargs=2,
                        help='Specify number of retries and wait time in minutes (e.g., -r 10 15)')

    args = parser.parse_args()

    # Validate retry arguments
    total_wait_time = 0
    if args.retry:
        retries, wait_minutes = args.retry
        total_wait_time = retries * wait_minutes
        if total_wait_time > 1439:  # 23 hours and 59 minutes
            logging.error("Total wait time exceeds 23 hours and 59 minutes. Please reduce retries or wait time.")
            return

    # If delete argument is provided
    if args.delete:
        if args.last_days:
            delete_batch_files(args.last_days, args.directory)
        elif args.specific_date:
            delete_file(specific_date=args.specific_date, download_dir=args.directory)
        else:
            delete_file(offset=args.offset, download_dir=args.directory)
    else:
        if args.specific_date:
            download_ephemeris_file(get_day_of_year(specific_date=args.specific_date), args.directory, 
                                     retries if args.retry else 0, wait_minutes if args.retry else 0)
        elif args.last_days:
            download_batch_files(args.last_days, args.directory, 
                                 retries if args.retry else 0, wait_minutes if args.retry else 0)
        else:
            download_ephemeris_file(get_day_of_year(args.offset), args.directory, 
                                     retries if args.retry else 0, wait_minutes if args.retry else 0)

if __name__ == "__main__":
    main()
