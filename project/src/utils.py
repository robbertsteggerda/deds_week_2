from datetime import datetime
import re
from utils import *

def strip_time_from_string(input_string):
    # Regular expression to match time in the format HH:MM:SS
    time_regex = r'\s\d{2}:\d{2}:\d{2}$'
    stripped_string = re.sub(time_regex, '', input_string)
    return stripped_string

def convert_date_format(date_str):
    # Parse the input date string
    date_obj = datetime.strptime(date_str, '%d-%m-%Y')
    # Convert date object to the desired format
    converted_date = date_obj.strftime('%Y-%m-%d')
    return converted_date

def striptime(date_str):
        return datetime.strptime(date_str, '%d-%m-%Y').date()

def escape_single_quotes(input_str):
    return input_str.replace("'", "''")