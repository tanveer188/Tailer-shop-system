from django.apps import AppConfig
from watson import search as watson

class CustomerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Customer'
    def ready(self):
        Customers = self.get_model("Customers")
        watson.register(Customers,fields=["mobileno","address","name","email"])
