from django.utils.translation import ugettext_lazy as _


DEVICE_STATUS_CHOICES = [
    ("available", _("Available")),
    ("reserved", _("Reserved")),
    ("unavailable", _("Unavailable")),
    ("removed", _("Removed")),
]
