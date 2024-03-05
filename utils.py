from datetime import datetime, timedelta
from zoneinfo import ZoneInfo 
import re

def _get_current_datetime():
  return datetime.now(ZoneInfo("America/Los_Angeles"))

def formatted_date(): 
  current_date = _get_current_datetime()
  return current_date.strftime("%y/%m/%d")

def formatted_previous_date():
  current_date = _get_current_datetime()
  prev = current_date - timedelta(days=1)
  return prev.strftime("%y/%m/%d")


def formatted_time(): 
  current_date = _get_current_datetime()
  return current_date.strftime("%I:%M%p")
  
def remove_a_tags(text):
  pattern = r'<a href="[^"]*">(.*?)</a>'
  cleaned_text = re.sub(pattern, r'\1', text)
  return cleaned_text