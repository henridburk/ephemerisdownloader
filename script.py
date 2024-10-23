import os
import subprocess
import argparse
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime, timedelta

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Set up logging configuration with TimedRotatingFileHandler
log_file_path = 'logs/gps_sdr_sim.log'
handler = TimedRotatingFileHandler(log_file_path, when="midnight", interval=1, backupCount=7)
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def generate_filename(offset):
    # Calculate the current day of the year
    today = datetime.now()
    target_date = today - timedelta(days=offset)
    
    # Get the day of the year for the target date
    day_of_year = target_date.timetuple().tm_yday
    current_year = today.year
    year_suffix = str(current_year)[-2:]  # Last two digits of the current year
    
    # Generate the filename based on the day of the year
    filename = f"brdc{day_of_year:03d}0.{year_suffix}n"
    logger.info(f"Generated filename: {filename} for offset: {offset}")
    return filename

def run_gps_sdr_sim(lat, lon, alt, offset):
    # Generate the filename based on the offset
    filename = generate_filename(offset)
    
    # Construct the command
    command = f"./gps-sdr-sim -e downloads/{filename} -l {lat},{lon},{alt} -b 8"
    
    logger.info(f"Executing command: {command}")

    # Execute the command
    try:
        subprocess.run(command, shell=True, check=True)
        logger.info("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing command: {e}")
        print(f"Error executing command: {e}")

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Run gps-sdr-sim with specified parameters.")
    parser.add_argument('-o', type=int, default=0, help='Offset for the day (0 for today, 1 for yesterday, etc.)')
    parser.add_argument('-l', type=str, required=True, help='Latitude, longitude, altitude (e.g., 111,222,333)')
    
    args = parser.parse_args()
    
    # Split latitude, longitude, altitude
    lat, lon, alt = map(float, args.l.split(','))
    
    # Run the GPS SDR simulation
    run_gps_sdr_sim(lat, lon, alt, args.o)

if __name__ == "__main__":
    main()

