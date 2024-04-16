from datetime import datetime
import isodate

def change_date_format(date):
    dt = datetime.fromisoformat(date.replace("Z", "+00:00"))
    mysql_datetime_str = dt.strftime("%Y-%m-%d %H:%M:%S")
    return mysql_datetime_str

def change_duration_format(duration):
    duration = isodate.parse_duration(duration)
    return int(duration.total_seconds())
