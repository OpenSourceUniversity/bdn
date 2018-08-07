import os
from django.core.management.base import BaseCommand
from django.conf import settings
from bdn.skill.models import Skill


class Command(BaseCommand):
    help = 'Imports standardized skills'

    def handle(self, *args, **options):
        skills_file_path = os.path.join(
            settings.BASE_DIR, 'data', 'all_standardized_skills.txt')
        number_of_imported = 0
        with open(skills_file_path, 'r') as f:
            skills = [_.strip() for _ in f.readlines()]
            skills_count = len(skills)
            for index, skill_name in enumerate(skills, 1):
                if index % 100 == 0:
                    self.stdout.write("Processed {}/{} skills".format(
                        index, skills_count))
                if len(skill_name) > 70:
                    continue
                skill, created = Skill.objects.get_or_create(name=skill_name)
                if created:
                    number_of_imported += 1
                if not skill.standardized:
                    skill.standardized = True
                    skill.save()
        self.stdout.write("Successfully imported {0} skills".format(
            number_of_imported))
