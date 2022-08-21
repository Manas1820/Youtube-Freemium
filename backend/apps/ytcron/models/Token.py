from django.db import models


class Token(models.Model):
    token_value = models.CharField(
        max_length=50, unique=True
    )  # To store the value in the token
    no_of_calls = models.PositiveIntegerField(
        default=0
    )  # To count the no of calls made using that
    is_valid = models.BooleanField(
        default=True
    )  # To check the validity of the token
