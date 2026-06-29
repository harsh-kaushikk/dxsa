#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TASK 1
# EXERCISE 1(B)

def max_digit(input_number):
    # If number is 0, maximum digit is 0.
    if input_number == 0:
        return 0

    max_found = 0

    # Use modulo and integer division to inspect each digit.
    # No strings are used, as required by the assignment.
    while input_number > 0:
        digit = input_number % 10
        if digit > max_found:
            max_found = digit
        input_number = input_number // 10

    return max_found


# Test example
assert max_digit(43521) == 5
