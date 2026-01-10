def is_empty(input):
    return input.strip() == ""

def check_year(input, accept_empty=False):
    # When accept_empty is True, return True if input is empty
    # This is for databases that fill in default values for empty year fields
    if accept_empty and is_empty(input):
        return True
    if not input.isdigit():
        return False
    year = int(input)
    return 0 < year <= 2100

def check_month(input, accept_empty=False):
    # When accept_empty is True, return True if input is empty
    # This is for databases that fill in default values for empty month fields
    if accept_empty and is_empty(input):
        return True
    if not input.isdigit():
        return False
    month = int(input)
    return 1 <= month <= 12

def check_season(input, accept_empty=False):
    if accept_empty and is_empty(input):
        return True
    if input.isdigit():
        return int(input.strip()) > 0
    return False


def main():
    print(check_season("2", accept_empty=True))

if __name__ == "__main__":
    main()

