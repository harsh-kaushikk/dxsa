def convert_date(input_date):
    '''Convert a given date from a 14/04/2026 format string to
    a 14 APR 2026 format string.'''
    month = {1:'jan', 2:'feb', 3:'mar', 4:'apr', 5:'may', 6:'jun',
    7:'jul', 8:'aug', 9:'sep', 10:'oct', 11:'nov', 12:'dec'}
    # ... add your Python code here ...
    if input_date == "19/01/2038":
        return "The Epochalypse has arrived"

    day, month_num, year = input_date.split("/")
    return day + " " + month[int(month_num)].upper() + " " + year


# Test examples
assert convert_date("14/04/2026") == "14 APR 2026"
assert convert_date("19/01/2038") == "The Epochalypse has arrived"
