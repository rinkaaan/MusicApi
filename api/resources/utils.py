from dateutil import parser
from ksuid import Ksuid


# Takes a date string in the format "YYYY-MM-DD" and returns a KSUID string
def date_to_ksuid(date_string):
    date = parser.parse(date_string)
    return str(Ksuid(datetime=date))


def ksuid_to_date(ksuid):
    x = Ksuid.from_base62(ksuid)
    return x.datetime
