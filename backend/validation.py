from datetime import date, datetime


def is_not_empty(value):
    return bool(value)


def is_in_range(value, low, high):
    try:
        num = int(value)
        return low <= num <= high
    except (TypeError, ValueError):
        return False


def parse_date(value):
    if isinstance(value, datetime):
        return value.date()
    elif isinstance(value, date):
        return value

    for date_format in ("%m-%d-%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(
                str(value),
                date_format,
            ).date()
        except ValueError:
            continue

    return None


def valid_due_date(value):
    due_date = parse_date(value)
    return due_date is not None and due_date >= date.today()


def valid_comp_date(value):
    completed_date = parse_date(value)
    return (
        completed_date is not None
        and completed_date <= date.today()
    )


def days_left(due_date):
    parsed_date = parse_date(due_date)
    if parsed_date is None:
        raise ValueError("Invalid due date.")
    return (parsed_date - date.today()).days


def is_diff(value):
    return is_in_range(value, 1, 5)


def is_positive_float(value):
    try:
        return float(value) > 0
    except (TypeError, ValueError):
        return False


def is_hours(value):
    return is_positive_float(value)
