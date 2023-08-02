from django.core.management import BaseCommand

from django.contrib.auth.models import User
from shopapp.models import Order

class Command(BaseCommand):
    """
    Creates order
    """
    def handle(self, *args, **kwargs):
        self.stdout.write("Create order")
        user = User.objects.get(username="admin")
        order = Order.objects.get_or_create(
            delivery_address="Street, house",
            promocode="SALE123",
            user=user,
        )
        self.stdout.write(f"Create order {order}")

