import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from bdn.category.models import Category


class Command(BaseCommand):
    help = 'Imports categories'

    def handle(self, *args, **options):
        categories_file_path = os.path.join(
            settings.BASE_DIR, 'data', 'category', 'industry_codes.csv')
        with open(categories_file_path, 'r') as categories_csv:
            categories_reader = csv.reader(
                categories_csv, delimiter=',', quotechar='"')
            for category_row in categories_reader:
                category_name = category_row[2]
                Category.objects.get_or_create(name=category_name)
