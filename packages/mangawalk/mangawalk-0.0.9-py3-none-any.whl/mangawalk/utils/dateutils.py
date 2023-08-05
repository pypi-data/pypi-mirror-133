from datetime import datetime, timedelta, timezone
from decimal import Decimal
import time

def created_at():
    """[summary]

    Returns:
        [type]: [description]
    """
    JST = timezone(timedelta(hours=+9), 'JST')
    timestamp = Decimal(time.time())
    today = datetime.now(JST).date()
    created_at = str(today.strftime("%Y%m%d"))
    return created_at

def times():
    """[summary]

    Returns:
        [type]: [description]
    """
    JST = timezone(timedelta(hours=+9), 'JST')
    timestamp = Decimal(time.time())
    today = datetime.now(JST).date()
    created_at = str(today.strftime("%Y%m%d"))
    created_at_unix = Decimal(time.mktime(today.timetuple()))
    last_created_at = str((today - timedelta(days=1)).strftime("%Y%m%d"))
    return {"timestamp": timestamp, "created_at": created_at, "created_at_unix": created_at_unix, "last_created_at": last_created_at}

