from datetime import datetime


def convert_time_to_scalar(date: datetime, min_date: datetime) -> int:
    """
    Convert time to scalar (seconds since min_date).

    Args:
        date: Input date as datetime object
        min_date: Minimum date as datetime object

    Returns:
        Number of seconds between date and min_date
    """
    return int((date - min_date).total_seconds())
