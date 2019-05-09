from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

from estimation.models import Holiday


class Estimation(object):
    estimation_type = None

    date = None
    step_2 = None
    step_3 = None

    allowed_estimation = ['delivery', 'return']
    NOT_ALLOWED = ["Saturday", "Sunday"]

    def __init__(self, date: str, estimation_type: str):
        self.estimation_type = self.is_allowed_estimation(estimation_type)
        self.date = date

    def is_allowed_estimation(self, estimation_type: str):
        if estimation_type in self.allowed_estimation:
            return estimation_type
        else:
            raise Exception

    def date_check(self):
        date_obj = parse(self.date)
        if self.weekend(date_obj):
            return None, date_obj.day, "Weekend is not allowed"

        elif self.holiday(date_obj):
            return None, self.holiday(date_obj), self.holiday(date_obj).first().name

        else:
            self.step_2 = self.find_day(date_obj + relativedelta(days=1))
            self.step_3 = self.find_day(self.step_2+relativedelta(days=1))

        return True, date_obj, "Normal Order"

    def find_day(self, date_obj):
        if self.holiday(date_obj) or self.weekend(date_obj):
            for x in range(1, 6):
                delta = relativedelta(days=x)
                if not self.holiday(date_obj) or not self.weekend(date_obj):
                    return date_obj+delta
        else:
            return date_obj

    def holiday(self, date_obj):
        return Holiday.objects.filter(date__year=date_obj.year,
                                      date__day=date_obj.day,
                                      date__month=date_obj.month)

    def weekend(self, date_obj):
        return date_obj.strftime("%A") in self.NOT_ALLOWED

    def estimate(self):
        allowed, estimate_date, reason = self.date_check()
        if not allowed:
            return None, estimate_date, reason

        return allowed, estimate_date, reason

    def delivery(self):
        allowed, estimate, reason = self.estimate()
        return {
            "order": f"{estimate.isoformat()}",
            "processing": f"{self.step_2.isoformat()}",
            "receive": f"{self.step_3.isoformat()}"
        }

    def pick_up(self):
        allowed, estimate, reason = self.estimate()

        return {
            "return": f"{estimate.isoformat()}",
            "processing": f"{self.step_2.isoformat()}",
            "unbooked": f"{self.step_3.isoformat()}"
        }
