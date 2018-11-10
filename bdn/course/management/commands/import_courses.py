import json
import csv
from django.core.management.base import BaseCommand
from bdn.course.models import Course
from bdn.provider.models import Provider
from bdn.skill.models import Skill
from bdn.industry.models import Industry
from bdn.course.management.commands.industry_ralations_to_linkedin import \
 LinkedinIndustryRelation


class Command(BaseCommand):
    help = 'Imports courses'

    def add_arguments(self, parser):
        parser.add_argument('--type')
        parser.add_argument('--file')
        parser.add_argument('--industry')

    def handle(self, *args, **options):
        industry_name = options['industry']
        file_path = options['file']
        industry = None
        is_csv = False
        if file_path is None:
            file_path = 'data/courses/courses.csv'
        if file_path[-3:] == 'csv':
            is_csv = True
            industry_linkedin = LinkedinIndustryRelation()
        if industry_name is not None and is_csv is False:
            industry, _ = Industry.objects.get_or_create(name=industry_name)

        with open(file_path) as f:
            if is_csv:
                courses = csv.reader(f, delimiter=',')
                print('dasdasdas')
            else:
                courses = json.load(f)
            for course in courses:
                if is_csv:
                    title = course[1]
                    description = ''
                    duration = None
                    external_link = course[6]
                    if isinstance(course[8], int):
                        duration = course[8]
                    image_url = course[9].strip()
                    if image_url[-3:] != 'jpg' and image_url[-3:] != 'png':
                        image_url = ''
                    if course[2].strip() == '' or course[1].strip() == '' or \
                       course[3].strip() == '' or course[5].strip() == '':
                        continue
                    provider, _ = Provider.objects.get_or_create(
                        name=course[2].strip()
                    )
                    tutor = course[3].strip().title()
                    try:
                        course_obj, _ = Course.objects.get_or_create(
                            title=title,
                            description=description,
                            external_link=external_link,
                            image_url=image_url,
                            duration=duration,
                            provider=provider,
                            tutor=tutor
                            )
                        industry_list = \
                            industry_linkedin.class_central(course[5])
                        if len(industry_list) > 0:
                            for industry_name in industry_list:
                                industry, _ = Industry.objects.get_or_create(
                                    name=industry_name
                                )
                                course_obj.industries.add(industry)
                    except Exception as e:
                        print(e)
                        continue
                else:
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
                            skill, _ = Skill.objects.get_or_create(
                                name__iexact=skill_name
                            )
                            course_obj.skills.add(skill)
                    except Exception:
                        continue
