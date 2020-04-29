import datetime


class Date:
    def todays_date(self):
        date_time = str(datetime.datetime.now())
        split_dt = date_time.split()
        today_date = split_dt[0]

        return today_date
