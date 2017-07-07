import datetime

weekdays = ['M', 'T', 'W', 'R', 'F', 'S', 'S']


def weekday_range(start_date, end_date, day_of_week):
    """
    Returns a generator of all the days between two date objects.

    Results include the start and end dates.
    """
    # If a datetime object gets passed in,
    # change it to a date so we can do comparisons.
    if isinstance(start_date, datetime.datetime):
        start_date = start_date.date()
    if isinstance(end_date, datetime.datetime):
        end_date = end_date.date()

    # Verify that the start_date comes after the end_date.
    if start_date > end_date:
        raise ValueError(
            'You provided a start_date that comes after the end_date.')

    # Jump forward from the start_date...
    while True:
        if weekdays[start_date.weekday()] == day_of_week:
            yield start_date
        # ... one day at a time ...
        start_date = start_date + datetime.timedelta(days=1)
        # ... until you reach the end date.
        if start_date > end_date:
            break
