from datetime import timedelta

def iter_dates(start, end):
    for i in range( (end-start).days ):
        yield start + timedelta(days=i)
