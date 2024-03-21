from datetime import datetime
import re
from utils import *

def strip_time_from_string(input_string):
    # Regular expression to match time in the format HH:MM:SS
    time_regex = r'\s\d{2}:\d{2}:\d{2}$'
    if(type(input_string) != str): return "NULL"
    stripped_string = re.sub(time_regex, '', input_string)

    if(stripped_string) == '': return
    return stripped_string

def convert_date_format(date_str):
    # Parse the input date string
    if(date_str == "NULL"): return 'NULL'
    date_obj = datetime.strptime(date_str, '%d-%m-%Y')
    # Convert date object to the desired format
    converted_date = date_obj.strftime('%Y-%m-%d')
    return converted_date

def striptime(date_str):
        if(date_str == "NULL"): return 'NULL'
        return datetime.strptime(date_str, '%d-%m-%Y').date()

def escape_single_quotes(input_str):
    return input_str.replace("'", "''")



def get_day(date_string):
    date_object = datetime.strptime(date_string, "%Y-%m-%d")

    # Extract the day
    day = date_object.day
    return day
def get_month(date_string):
    date_object = datetime.strptime(date_string, "%Y-%m-%d")

    # Extract the day
    month = date_object.month
    return month

def get_year(date_string):
    date_object = datetime.strptime(date_string, "%Y-%m-%d")

    # Extract the day
    year = date_object.year
    return year
