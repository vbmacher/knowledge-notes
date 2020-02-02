import datetime
import time
from sys import argv,exit


def enum_ranges(begin, end):
    first_day_to = end.replace(day=1)
    ranges = [(first_day_to, end)]

    until = first_day_to - datetime.timedelta(days=1)
    start = until.replace(day=1)
    if begin > start:
        start = begin

    while begin <= until:
        ranges += [(start, until)]
        until = start - datetime.timedelta(days=1)
        start = until.replace(day=1)
        if begin > start:
            start = begin

    return ranges

if __name__ == "__main__":

  FROM = datetime.datetime.strptime(argv[1], '%Y-%m-%d').date()
  TO = datetime.datetime.strptime(argv[2], '%Y-%m-%d').date()

  if FROM > TO:
    print("Error: FROM > TO")
    exit(1)


  for (begin, end) in reversed(enum_ranges(FROM, TO)):
      print(begin, end)

