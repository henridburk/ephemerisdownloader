# !!! STILL NEED TO ADD README CONTENTS FOR OTHER 2 SCRIPTS. 1 OF THEM CONVERTS THE EPHEMERIS FILE FROM .xxn to a .bin file. the other one simply loops this to the sdr. 

# Ephemeris Downloader
## Overview
The Ephemeris Downloader is a Python script that allows users to download GNSS ephemeris files from NASA's CDDIS archive. The script provides options to download specific files based on the current date, past dates, or a batch of files for a specified number of days. Additionally, users can delete specific files as needed.

## Features
- Download Specific Files: Download ephemeris files for today or any previous day based on an offset or a specific date.
- Batch Downloads: Efficiently batch download ephemeris files for the last X days in one command, making it easy to gather multiple files quickly.
- Delete Files: Delete specific ephemeris files based on a date or an offset. This helps manage storage and remove outdated files.
- Custom Directory: Specify a custom directory for downloading or deleting files, allowing better organization of downloaded data.
- Error Handling and Logging: Automatic logging of all download and delete operations, including errors. Logs are stored in a logs/ directory, rotated daily, and maintained for the last 7 days.
- Flexible Date Handling: Support for specific dates in dd-mm-yyyy format for precise control over file management.
- Retry Functionality: Implement retry logic for download attempts, allowing the user to specify the number of retries and the wait time between attempts. This ensures robustness in case of temporary network issues or file unavailability.

## Requirements
- Python 3.x: Ensure you have Python version 3.6 or higher installed on your machine.
- Dependencies: 
   - ```argparse``` (Included in the standard library) for parsing command-line arguments.
   - ```os``` (Included in the standard library) for interacting with the operating system (file management).
   - ```datetime``` (Included in the standard library) for handling date and time operations.
   - ```requests``` For making HTTP requests to download ephemeris files.
   - ```logging``` (Included in the standard library) for logging operations and error handling.

To install the required libraries, run:

For Windows (If you are using Python 3 and pip is not linked to Python 3, you may need to use pip3 instead):
```
pip install requests
```
For Debian/Ubuntu:
```
sudo apt install python3-pip
```
For CentOS/RHEL:
```
sudo yum install python3-pip
```
## Setup
1. Clone or download this repository to your local machine.
2. Ensure you have Python installed.
3. Install the required libraries
4. Set up your .netrc file for authentication with NASA’s server, as required by the script. For more information, visit: [Creating a .netrc file.](https://cddis.nasa.gov/Data_and_Derived_Products/CreateNetrcFile.html)

## Logging
The script automatically logs all download and delete operations, including errors, into daily log files stored in the logs/ directory. Logs are rotated daily, and only the logs from the last 7 days are kept.

## Usage
To display the help section with all available arguments, you can run:
```
python ephemerisdownloader.py -h
```
Command-Line Arguments
- -o OFFSET or --offset OFFSET: Specify an offset in days from today (0 for today, 1 for yesterday, etc.). Default is 0.
- -d or --delete: Flag to indicate that you want to delete the file for the given offset or specific date.
- -s SPECIFIC_DATE: Provide a specific date in dd-mm-yyyy format for download or deletion.
- -l LAST_DAYS: Download or delete files for the last X days.
- -dir DIRECTORY: Specify a custom directory for downloading or deleting files. If not provided, it defaults to downloads/.
- -r RETRIES MINUTES_BETWEEN: Specify the number of retries and the wait time in minutes between attempts for downloads. The maximum wait time should not exceed 23 hours and 59 minutes total.

## Command Examples and Combinations
### Download Examples
#### Download today's ephemeris file:
```
python ephemerisdownloader.py
```
#### Download today's ephemeris file with 5 retries at 15 minute intervals:
```
python ephemerisdownloader.py -r 5 15
```
#### Download ephemeris file for a specific date:
```
python ephemerisdownloader.py -s 15-06-2024
```
#### Download ephemeris file for yesterday:
```
python ephemerisdownloader.py -o 1
```
#### Batch download ephemeris files for the last 5 days:
```
python ephemerisdownloader.py -l 5
```
#### Download ephemeris file for 3 days ago into a custom directory:
```
python ephemerisdownloader.py -o 3 -dir /path/to/my/directory
```
#### Download ephemeris file for 3 days ago into a custom directory with 5 retries at 15 minute intervals:
```
python ephemerisdownloader.py -o 3 -dir /path/to/my/directory -r 5 15
```
### Delete Examples
#### Delete the ephemeris file for today:
```
python ephemerisdownloader.py -d -o 0
```
#### Delete the ephemeris file for yesterday:
```
python ephemerisdownloader.py -d -o 1
```
#### Batch delete ephemeris files for the last 7 days:
```
python ephemerisdownloader.py -d -l 7
```
### Combined Operations
#### Download file for a specific date and then delete it:
```
python ephemerisdownloader.py -s 20-09-2024 && python ephemerisdownloader.py -d -s 20-09-2024
```
#### Download file for today and delete the file from 5 days ago:
```
python ephemerisdownloader.py && python ephemerisdownloader.py -d -o 5
```
## Summary of Command-Line Argument Combinations
- -o OFFSET: Specify the number of days from today. For example, -o 1 for yesterday, -o 10 for 10 days ago.
- -d or --delete: Use this flag to delete files. You can specify the file to delete with -o or -s.
- -s SPECIFIC_DATE: Specify a date in dd-mm-yyyy format for downloading or deleting a specific file.
- -l LAST_DAYS: Download or delete files for the last X days.
- -dir DIRECTORY: Specify a custom directory for storing or deleting files. Defaults to downloads/ if not provided.
- -r RETRIES MINUTES_BETWEEN: Set the number of retries and the wait time (in minutes) between attempts when downloading files. The maximum wait time should not exceed 23 hours and 59 minutes in total.

## Note
When combining commands, ensure that the order of execution is appropriate, as the shell processes commands sequentially. For instance, downloading a file and then immediately deleting it in a single command sequence may not yield the expected outcome if the file hasn't finished downloading.

## Automating the Ephemeris Downloader Script
To automate the downloading and management of ephemeris files, you can set up scheduled tasks using cron on Linux or Task Scheduler on Windows. This enables the script to run at specified intervals, ensuring you always have the latest ephemeris data.

### Using Cron Jobs on Linux
Cron is a time-based job scheduler in Unix-like operating systems. You can use it to run the Ephemeris Downloader script at regular intervals.

#### Setting Up a Cron Job
1. Open the Terminal.

2. Edit the Crontab File: Run the following command to open the crontab file in the default text editor:

```
crontab -e
```
3. Add a Cron Job: In the crontab file, you can specify when to run your script. The format is as follows:

```
* * * * * /usr/bin/python3 /path/to/your/script/ephemerisdownloader.py
```
#### The five asterisks represent:

- Minute (0 - 59)
- Hour (0 - 23)
- Day of Month (1 - 31)
- Month (1 - 12)
- Day of Week (0 - 7) (Sunday is both 0 and 7)
#### Example Cron Jobs:
#### To run the script every day at 6 AM to download today’s ephemeris file:
```
0 6 * * * /usr/bin/python3 /path/to/your/script/ephemerisdownloader.py
``` 

#### To run the script every day at 6 AM to delete the ephemeris file for yesterday:
```
0 6 * * * /usr/bin/python3 /path/to/your/script/ephemerisdownloader.py -d -o 1
```

#### To run the script every Sunday at midnight to delete files older than 7 days:
```
0 0 * * 0 /usr/bin/python3 /path/to/your/script/ephemerisdownloader.py -d -l 7
``` 
4. Save and Exit: Save your changes and exit the text editor. The cron job will now be scheduled to run at the specified times.

### Using Task Scheduler on Windows
Task Scheduler is a Windows tool that allows you to schedule tasks and automate processes.

#### Setting Up a Scheduled Task
1. Open Task Scheduler:

- Press ```Win + R```, type ```taskschd.msc```, and hit Enter.

2. Create a New Task:

- In the right panel, click Create Basic Task.
3. Name Your Task:

- Give your task a name and description, then click Next.
4. Set the Trigger:

- Choose how often you want the task to run (Daily, Weekly, Monthly, etc.), then click Next.
- Follow the prompts to set the specific time and frequency.

5. Set the Action:

- Choose Start a program and click Next.

- In the "Program/script" field, enter the path to your Python executable (e.g., ```C:\Python39\python.exe```).

- In the "Add arguments (optional)" field, enter the path to your script along with any arguments you want to use. Here are some examples:
   - To download the ephemeris file for today:
   ```
   C:\path\to\your\script\ephemerisdownloader.py
   ```
   - To delete the ephemeris file for yesterday:
   ```
   C:\path\to\your\script\ephemerisdownloader.py -d -o 1
   ```
   - To batch delete ephemeris files for the last 30 days:
   ```
   C:\path\to\your\script\ephemerisdownloader.py -d -l 30
   ```
6. Finish the Task:

- Review your settings and click Finish to create the task.

## Example Use Cases
Daily Downloads: Automate the script to run every morning at 6 AM to download the latest ephemeris file for the day, ensuring you have the latest data for your applications.

Batch Deletion: Schedule the script to run weekly to delete old ephemeris files, helping you manage disk space effectively by keeping only the most recent files.

Combined Operations: Use cron jobs or Task Scheduler to run the download and delete functions in succession, ensuring that you download the latest files while removing outdated ones automatically.
