import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from bdn.industry.models import Industry


class Command(BaseCommand):
    help = 'Imports industries'

    def handle(self, *args, **options):
        industries_file_path = os.path.join(
            settings.BASE_DIR, 'data', 'industry', 'industry_codes.csv')
        with open(industries_file_path, 'r') as industries_csv:
            industries_reader = csv.reader(
                industries_csv, delimiter=',', quotechar='"')
            for industry_row in industries_reader:
                industry_name = industry_row[2]
                Industry.objects.get_or_create(name=industry_name)
