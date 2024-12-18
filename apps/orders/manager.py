from datetime import timedelta
from django.utils.timezone import now
from django.db import models


class RobotManager(models.Manager):
    def robots_created_last_week(self):
        start_date = now() - timedelta(days=7)
        return self.filter(created__gte=start_date)
