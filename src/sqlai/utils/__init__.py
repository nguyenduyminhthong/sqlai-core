from datetime import datetime
from pytz import timezone


def get_formatted_time():
    current_time = datetime.now(tz=timezone("Asia/Ho_Chi_Minh"))
    formatted_time = current_time.strftime("%Y/%m/%d - %H:%M:%S")
    return formatted_time
