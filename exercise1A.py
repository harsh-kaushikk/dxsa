#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TASK 1
# EXERCISE 1(A)

def convert_date(input_date):
    # Dictionary stores month number and short month name.
    month = {1:'jan', 2:'feb', 3:'mar', 4:'apr', 5:'may', 6:'jun',
             7:'jul', 8:'aug', 9:'sep', 10:'oct', 11:'nov', 12:'dec'}

    # Required easter egg from assignment.
    if input_date == "19/01/2038":
        return "The Epochalypse has arrived"

    # Extract day, month, year from dd/mm/yyyy.
    day = input_date[0:2]
    month_number = int(input_date[3:5])
    year = input_date[6:10]

    # Return in required format: DD MON YYYY
    return day + " " + month[month_number].upper() + " " + year


# Test examples
assert convert_date("14/04/2026") == "14 APR 2026"
assert convert_date("19/01/2038") == "The Epochalypse has arrived"

# Assert checks expected output is correct.
