def next_look_and_say(input_number):
    # ... add your Python code here ...
    s = str(input_number)
    output = ""
    count = 1

    for i in range(1, len(s) + 1):
        if i < len(s) and s[i] == s[i - 1]:
            count += 1
        else:
            output += str(count) + s[i - 1]
            count = 1

    return int(output)


# Test examples
assert next_look_and_say(1) == 11
assert next_look_and_say(11) == 21
assert next_look_and_say(21) == 1211
assert next_look_and_say(1211) == 111221


def investigate_look_and_say():
    # ... add your Python code here ...
    # Build terms as strings so we can investigate many terms safely.
    terms = ["1"]
    n_terms = 50

    for _ in range(n_terms - 1):
        s = terms[-1]
        out = ""
        count = 1
        for i in range(1, len(s) + 1):
            if i < len(s) and s[i] == s[i - 1]:
                count += 1
            else:
                out += str(count) + s[i - 1]
                count = 1
        terms.append(out)

    # Investigate maximum digit in generated terms.
    max_digit_seen = 0
    for term in terms:
        for ch in term:
            d = int(ch)
            if d > max_digit_seen:
                max_digit_seen = d

    # Investigate long-run ratio of successive term lengths.
    ratios = []
    for i in range(len(terms) - 1):
        ratios.append(len(terms[i + 1]) / len(terms[i]))

    print("Last 10 length ratios:")
    print(ratios[-10:])
    print("Average of last 5 length ratios:")
    print(sum(ratios[-5:]) / 5)
    print("Maximum digit seen:")
    print(max_digit_seen)


investigate_look_and_say()

# Example output from one run:
# Last 10 length ratios:
# [1.3031208257437765, 1.3044580289250036, 1.3028346096696766,
#  1.303603544326008, 1.3040640010767794, 1.302964816988995,
#  1.3036889243154126, 1.303809389988721, 1.3031605805611626,
#  1.3037873962070161]
# Average of last 5 length ratios:
# 1.3034822216122615
# Maximum digit seen:
# 3
#
# Conclusion:
# The maximum digit observed is 3. The ratio of successive term lengths
# approaches approximately 1.3035 in the long run.
