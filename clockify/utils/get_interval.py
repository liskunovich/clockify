from datetime import datetime, timedelta
from ..enums import TimeInterval


def get_interval(start_date: datetime, interval: TimeInterval) -> tuple[datetime, datetime]:
    return start_date - get_timedelta(interval), start_date


def get_timedelta(interval: TimeInterval) -> timedelta:
    match interval:
        case TimeInterval.WEEK:
            return timedelta(weeks=1)
        case TimeInterval.TWO_WEEKS:
            return timedelta(weeks=2)
        case TimeInterval.THREE_WEEKS:
            return timedelta(weeks=3)
        case TimeInterval.MONTH:
            return timedelta(weeks=4)
