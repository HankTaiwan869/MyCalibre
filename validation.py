def is_empty(input):
    return input.strip() == ""

def check_year(input):
    if is_empty(input):
        return True
    if not input.isdigit():
        return False
    year = int(input)
    return 0 < year <= 2100

def check_month(input):
    if is_empty(input):
        return True
    if not input.isdigit():
        return False
    month = int(input)
    return 1 <= month <= 12

