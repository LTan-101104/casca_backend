import re

def format_date(date_str):
    return re.sub(r"(\d{1,2})[ -]([A-Za-z]{3}).*", r"\1-\2", date_str)

# Test cases
dates = ["04 Nov 19", "12-Mar-2019", "11 Oct"]
formatted_dates = [format_date(date) for date in dates]

print(formatted_dates)