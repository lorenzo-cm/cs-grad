from datetime import datetime


#! converter para ao inves de UNIX time 1970 para menor data do dataset

def convert_time_to_scalar(date: str, format: str, min_date: str) -> int:
    """
    Possible formats:
    - 'YYYY-MM-DD HH:MM:SS'
    - 'YYYY-MM-DD'
    - 'YYYY/MM/DD HH:MM:SS'
    - 'YYYY/MM/DD'
    - 'DD-MM-YYYY HH:MM:SS'
    """
    dt = datetime.strptime(date, format)
    return int(dt.timestamp())
