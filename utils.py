from datetime import datetime 
import re

def _get_current_datetime():
  return datetime.now()

def formatted_date(): 
  current_date = _get_current_datetime()
  return current_date.strftime("%y/%m/%d")

def formatted_time(): 
  current_date = _get_current_datetime()
  return current_date.strftime("%I:%M%p")
  
def remove_a_tags(text):
  pattern = r'<a href="[^"]*">(.*?)</a>'
  cleaned_text = re.sub(pattern, r'\1', text)
  return cleaned_text