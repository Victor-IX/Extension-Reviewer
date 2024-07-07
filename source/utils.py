def has_lower_upper_pair(s):
    for i in range(len(s) - 1):
        if s[i].islower() and s[i + 1].isupper():
            return True
    return False