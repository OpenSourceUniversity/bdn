import json
from django.core.management.base import BaseCommand
from bdn.course.models import Provider, Course, Category, Skill


class Command(BaseCommand):
    help = 'Imports courses'

    def add_arguments(self, parser):
        parser.add_argument('--file')
        parser.add_argument('--category')

    def handle(self, *args, **options):
        category_name = options['category']
        file_path = options['file']
        category, _ = Category.objects.get_or_create(name=category_name)

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
                    course_obj = Course(
                        title=title,
                        description=description,
                        external_link=external_link,
                        provider=provider,
                        tutor=tutor
                    )
                    course_obj.save()

                    course_obj.categories.add(category)

                    for skill_name in course['skills']:
                        skill, _ = Skill.objects.get_or_create(name=skill_name)
                        course_obj.skills.add(skill)
                except Exception:
                    continue
