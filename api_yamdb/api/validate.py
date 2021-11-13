import datetime as dt

from rest_framework import serializers


def validate_year(value):
    """Check the year."""
    year = dt.date.today().year
    if value > year:
        raise serializers.ValidationError('Invalid value of year')
    return value
