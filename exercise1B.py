def max_digit(input_number):
    # ... add your Python code here ...
    max_found = 0

    while input_number > 0:
        digit = input_number % 10
        if digit > max_found:
            max_found = digit
        input_number = input_number // 10

    return max_found


# Test example
assert max_digit(43521) == 5
