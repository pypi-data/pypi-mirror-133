import datetime

FORMAT_DATETIME = '%Y-%m-%d %H:%M:%S'
FORMAT_DATE = '%Y-%m-%d'


def now():
    return datetime.datetime.now()


def today():
    return format(now(), FORMAT_DATE)


def current():
    return format(now(), FORMAT_DATETIME)


def strftime(date: datetime.datetime, fmt: str = FORMAT_DATETIME):
    return date.strftime(fmt)


def strptime(value: str, fmt: str = FORMAT_DATETIME):
    return datetime.datetime.strptime(value, fmt)
