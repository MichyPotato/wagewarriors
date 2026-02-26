import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from map.models import Location


class Command(BaseCommand):
    help = 'Load location data (city, state, country) from CSV file'

    def handle(self, *args, **kwargs):
        data_file = settings.BASE_DIR / 'data' / 'filtered_cities_filtered.csv'
        keys = ('city', 'state', 'country', 'latitude', 'longitude')  # CSV columns to gather data from

        records = []
        with open(data_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                records.append({k: row[k] for k in keys})

        for record in records:
            Location.objects.get_or_create(
                city=record['city'],
                state=record['state'],
                country=record['country'],
                latitude=float(record['latitude']),
                longitude=float(record['longitude'])
            )