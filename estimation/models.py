from django.db import models

# Create your models here.

HOLIDAY_TYPE_CHOICES = (
    ('public', 'Public Holiday'),
    ('national', 'National Holiday'),
    ('religion', 'Religion Holiday'),
)


class Holiday(models.Model):
    date = models.DateTimeField(unique=True)
    name = models.CharField(max_length=256)
    holiday_type = models.CharField(choices=HOLIDAY_TYPE_CHOICES, max_length=12)

    @property
    def weekday(self):
        return self.date.weekday()
