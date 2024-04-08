from datetime import datetime
from database.dbHandler import *
import pytz

def current_date_and_hour():
    timezone_br = pytz.timezone('America/Sao_Paulo')
    now = datetime.now(timezone_br)
    date = now.strftime('%d/%m/%Y')
    current_hour_and_minute = now.strftime('%H:%M')
    return date, current_hour_and_minute


def is_first_date_before_second(date1, date2):
    """
    Check if the first date comes before the second date.

    Parameters:
    date1 (str): First date in the format "day/month/year"
    date2 (str): Second date in the format "day/month/year"

    Returns:
    bool: True if the first date is before the second, False otherwise
    """

    # Convert string dates to datetime objects
    date_format = "%d/%m/%Y"
    datetime1 = datetime.strptime(date1, date_format)
    datetime2 = datetime.strptime(date2, date_format)
    
    # Compare the two dates
    return datetime1 < datetime2


def format_date_day_month_year(date):
    date_parts = date.split('/')
    
    date_now = datetime.now().strftime('%d/%m/%Y')
    
    date_now_parts = date_now.split('/')
    
    if len(date_parts) == 1:
        parts = [date_parts[0], date_now_parts[1], date_now_parts[2]]
    
    elif len(date_parts) == 2:
        parts = [date_parts[0], date_parts[1], date_now_parts[2]]
    
    else:
        parts = [date_parts[0], date_parts[1], date_parts[2]]
        
    return '/'.join(parts)


def convert_date(date_str):
    """Converts date DD-MM-YYYY or DD/MM/YYYY into DD/MM/YYYY

    Args:
        date_str (str): input date as a string

    Returns:
        str: formatted date string
    """
    if '-' in date_str:
        date_str = date_str.replace('-', '/')

    # Split the date into day, month, and year
    day, month, year = date_str.split('/')

    # Create the new date format
    formatted_date = f"{day}/{month}/{year}"
    return formatted_date


def is_valid_date(date_str):
    "Verify if the date is valid"
    try:
        date = datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        return False  # The date format is incorrect
    
    today = datetime.now()
    return date >= today # If date is in the past, return False, else True



def get_dt(db:DatabaseHandler, id:str):
   # Set timezone
    utc_minus_3 = pytz.timezone('Etc/GMT+3')  # Note the inversion: GMT+3 corresponds to UTC-3
    dt:datetime = db.get_datetime(id)
    current_time = datetime.now(utc_minus_3)
    if dt is not None:
        if dt.tzinfo is None:
            dt = utc_minus_3.localize(dt)
        print(f"Current time: {current_time}")
        time_difference = current_time - dt
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"{time_difference.days} days, {hours} hours, {minutes} minutes, {seconds} seconds")

        return time_difference, hours, minutes, seconds
    else:
        print("no current datetime in database")
        return None, None, None, None
