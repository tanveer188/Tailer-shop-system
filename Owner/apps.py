from django.apps import AppConfig
from watson import search as watson

class OwnerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Owner'
    def ready(self):
        Work = self.get_model("Work")
        watson.register(Work,fields=["billno","customer","date","cost"])