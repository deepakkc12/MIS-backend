from datetime import datetime,timedelta
import os
import random  # For handling file paths and extensions
from django.conf import settings  # To access Django settings, such as MEDIA_ROOT
from django.core.files.storage import default_storage  # For file storage operations
from django.core.files.base import ContentFile  # To handle file content
from django.utils.text import get_valid_filename
import pytz  # To sanitize the file name
# from dateutil.relativedelta import relativedelta




# def get_future_date_after_months(months: int) -> str:
#     """Returns the date after the current date by adding a specified number of months in 'YYYY-MM-DD' format."""
#     current_date = datetime.now()
#     future_date = current_date + relativedelta(months=months)
#     return future_date.strftime("%Y-%m-%d")



def get_current_date() -> str:
    """Returns the current date in 'YYYY-MM-DD' format."""

    # malaysia_tz = pytz.timezone("Asia/Kuala_Lumpur")
    malaysia_time = datetime.now()
    return malaysia_time.strftime("%Y-%m-%d")
    # return datetime.now().strftime("%Y-%m-%d")
def get_past_date(difference=30, date1=None) -> str:
    """Returns the date 'difference' days before the given date or today, in 'YYYY-MM-DD' format."""
    
    date_format = "%Y-%m-%d"
    
    if date1:
        reference_date = datetime.strptime(date1, date_format)  # Convert string to datetime
    else:
        reference_date = datetime.now()  # Use current date if no input date is provided
    
    past_date = reference_date - timedelta(days=difference)  # Subtract the difference
    return past_date.strftime(date_format)

def get_day_difference(date1: str, date2: str) -> int:
    """Returns the absolute difference in days between two dates in 'YYYY-MM-DD' format."""
    date_format = "%Y-%m-%d"
    d1 = datetime.strptime(date1, date_format)
    d2 = datetime.strptime(date2, date_format)
    return abs((d2 - d1).days)

def get_yesterday_date() -> str:
    """Returns yesterday's date in 'YYYY-MM-DD' format."""
    
    malaysia_tz = pytz.timezone("Asia/Kuala_Lumpur")
    malaysia_time = datetime.now() - timedelta(days=1)
    return malaysia_time.strftime("%Y-%m-%d")

def get_current_time() -> str:
    """Returns the current time in 'HH:MM:SS' format."""
    return datetime.now().strftime("%H:%M:%S")

def get_date_one_week_later() -> str:
    """Returns the date one week after the current date in 'YYYY-MM-DD' format."""
    one_week_later = datetime.now() + timedelta(weeks=1)
    return one_week_later.strftime("%Y-%m-%d")


def get_date_weak_before(weeks = 1) -> str:
    """Returns the date one week after the current date in 'YYYY-MM-DD' format."""

    malaysia_tz = pytz.timezone("Asia/Kuala_Lumpur")
    week_before = datetime.now(malaysia_tz) - timedelta(weeks=weeks)
    return week_before.strftime("%Y-%m-%d")

def get_numeric_current_time_representation():
    """
    Convert a time object to a numeric representation for SQL storage.
    Example: 14:30 becomes 1430.00

    """
    time_obj = datetime.strptime("14:30", "%H:%M").time() 
    return float(f"{time_obj.hour}{time_obj.minute:02d}.00")


def save_file(file, file_name_without_ext, file_type):
    """
    Save a file to the appropriate directory based on the file type.
    
    :param file: The file object to save.
    :param file_name_without_ext: Name of the file without extension.
    :param file_type: Type of the file (image, pdf, excel).
    :return: Dictionary with success status and file path or error message.
    """
    
    # Allowed extensions based on file type
    ALLOWED_EXTENSIONS = {
        'image': ['.jpg', '.jpeg', '.png', '.gif'],
        'excel': ['.xls', '.xlsx'],
        'pdf': ['.pdf']
    }
    
    # Check if file type is valid and get allowed extensions for the type
    allowed_extensions = ALLOWED_EXTENSIONS.get(file_type.lower())
    if allowed_extensions is None:
        return {'error': 'Invalid file type provided.'}
    
    # Extract file extension and validate it
    file_extension = os.path.splitext(file.name)[-1].lower()
    if file_extension not in allowed_extensions:
        return {'error': f'Invalid file extension. Allowed extensions: {", ".join(allowed_extensions)}'}
    
    # Ensure filename is safe for storage
    valid_filename = get_valid_filename(file_name_without_ext) if file_name_without_ext else get_valid_filename(file.name)
    
    complete_filename = f"{valid_filename}{file_extension}"
    
    # Construct the full file path
    path = os.path.join(file_type,'send', complete_filename)
    full_path = os.path.join(settings.MEDIA_ROOT, path)
    
    # Check and delete any existing file at the same path
    if default_storage.exists(full_path):
        default_storage.delete(full_path)
    
    # Save the new file
    try:
        default_storage.save(full_path, ContentFile(file.read()))
    except Exception as e:
        return {'error': f'Error saving file: {str(e)}'}
    
    return {'success': True, 'file_path': path}


def _generate_code(prefix: str = "", length: int = 14):

        datetime_part = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        
        random_part_length = max(0, length - len(prefix) - len(datetime_part))
        
        # Generate a random number with the calculated length
        random_part = ''.join(random.choices("0123456789", k=random_part_length))
        
        # Combine prefix, datetime part, and random part
        unique_code = f"{prefix}{datetime_part}{random_part}"

        print(unique_code[:length])
        # Truncate or pad the code to match the desired length
        return int(unique_code[:length])