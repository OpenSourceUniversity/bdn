import json
from django.core.management.base import BaseCommand
from bdn.course.models import Course
from bdn.provider.models import Provider
from bdn.skill.models import Skill
from bdn.industry.models import Industry


class Command(BaseCommand):
    help = 'Imports courses'

    def add_arguments(self, parser):
        parser.add_argument('--file')
        parser.add_argument('--industry')

    def handle(self, *args, **options):
        industry_name = options['industry']
        file_path = options['file']
        industry = None
        if industry_name is not None:
            industry, _ = Industry.objects.get_or_create(name=industry_name)

        with open(file_path) as f:
            courses = json.load(f)
            for course in courses:
                title = course['title']
                description = course['about']
                external_link = course['courseLink']
                provider, _ = Provider.objects.get_or_create(
                    name=course['provider'])
                tutor = course['tutor']

                try:
                    course_obj, _ = Course.objects.get_or_create(
                        title=title,
                        description=description,
                        external_link=external_link,
                        provider=provider,
                        tutor=tutor
                    )
                    if industry is not None:
                        course_obj.industries.add(industry)

                    for skill_name in course['skills']:
                        skill, _ = Skill.objects.get_or_create(name=skill_name)
                        course_obj.skills.add(skill)
                except Exception:
                    continue
