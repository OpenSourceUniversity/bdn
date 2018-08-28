import json
from django.core.management.base import BaseCommand
from bdn.course.models import Course
from bdn.provider.models import Provider
from bdn.skill.models import Skill
from bdn.industry.models import Industry
from bdn.company.models import Company
from bdn.auth.models import User
from faker import Faker
from bdn.profiles.models import Profile
import random

HEXADECIMAL_STR = '0123456789abcdef'
SKILLS = ['Python', 'Django', 'Java', '.NET', 'Project Management', 'Design']


class Command(BaseCommand):
    help = 'Import profiles'

    def add_arguments(self, parser):
        parser.add_argument('--learners')
        parser.add_argument('--businesses')
        parser.add_argument('--academies')
        parser.add_argument('--max_certificates')
        parser.add_argument('--max_courses')
        parser.add_argument('--max_jobs')

    def handle(self, *args, **options):
        countLearners = 1
        countBusinesses = 1
        countAcademies = 5
        max_certificates = 0
        max_courses = 0
        max_jobs = 0
        if options['learners']:
            countLearners = int(options['learners'])
        if options['businesses']:
            countBusinesses = int(options['businesses'])
        if options['academies']:
            countAcademies = int(options['academies'])
        if options['max_certificates']:
            max_certificates = int(options['max_certificates'])
        if options['max_courses']:
            max_courses = int(options['max_courses'])
        if options['max_jobs']:
            max_jobs = int(options['max_jobs'])
        fake_users = int(countLearners) + int(countBusinesses) + \
            int(countAcademies)
        faker = Faker()
        random_generator = random.SystemRandom()
        for profile in range(fake_users):
            eth_wallet = '0x'
            for _ in range(40):
                if random.choice('01') == '0':
                    eth_wallet += random.choice(HEXADECIMAL_STR).lower()
                else:
                    eth_wallet += random.choice(HEXADECIMAL_STR).upper()
            user, _ = User.objects.get_or_create(
                username=eth_wallet)
            try:
                if int(profile) < int(countLearners):
                    profile_obj = Profile.objects.get(user=user)
                    profile_obj.active_profile_type = 1
                    profile_obj.first_name = faker.name().split()[0]
                    profile_obj.last_name = faker.name().split()[1]
                    profile_obj.learner_email = faker.email()
                    profile_obj.learner_position = faker.job()
                    profile_obj.learner_specialisation = "Specialization ..."
                    profile_obj.learner_about = faker.text()
                    profile_obj.learner_country = faker.country()
                    profile_obj.save()
                    print('User eth: ' + str(eth_wallet) + ' was created!')
                elif int(profile) < (fake_users-int(countAcademies)):
                    business_obj = Profile.objects.get(user=user)
                    company, _ = Company.objects.get_or_create(user=user)
                    business_obj.active_profile_type = 3
                    business_obj.company_name = faker.company()
                    business_obj.company_website = 'https://www.business.com'
                    business_obj.company_email = faker.email()
                    business_obj.company_country = faker.country()
                    if random.choice('01') == '0':
                        business_obj.company_verified = True
                    else:
                        business_obj.company_verified = False
                    business_obj.save()
                    print('Business eth: ' + str(eth_wallet) + ' was created!')
                elif int(profile) < fake_users:
                    academy_obj = Profile.objects.get(user=user)
                    academy_obj.active_profile_type = 2
                    academy_obj.academy_name = faker.company()
                    provider, _ = Provider.objects.get_or_create(
                        name=academy_obj.academy_name)
                    industry, _ = Industry.objects.get_or_create(
                        name='Accounting')
                    academy_obj.academy_website = 'https://www.academy.com'
                    academy_obj.academy_email = faker.email()
                    academy_obj.academy_country = faker.country()
                    if random.choice('01') == '0':
                        academy_obj.academy_verified = True
                    else:
                        academy_obj.academy_verified = False
                    if int(max_courses) > 0:
                        nr_courses = \
                            int(random_generator.randint(0, int(max_courses)))
                        for _ in range(0, nr_courses):
                            course_obj = Course.objects.create(
                                title='Course titl',
                                description=faker.text(),
                                external_link='https://www.coursera.org/',
                                provider=provider,
                                tutor=academy_obj.academy_name
                            )
                            course_obj.industries.add(industry)
                            nr_skills = \
                                int(random_generator.randint(1, len(SKILLS)))
                            for skill_id in range(1, nr_skills):
                                skill, _ = Skill.objects.get_or_create(
                                    name=SKILLS[skill_id]
                                )
                                course_obj.skills.add(skill)
                    academy_obj.save()
                    print('Academy eth: ' + str(eth_wallet) + ' was created!')
                    if nr_courses > 0:
                        print('--> Courses added')
            except Exception:
                continue
        print('Generation of face profiles finished successfully!')
        print(str(Profile.objects.count()) + ' profiles stored in the DB')
        return
