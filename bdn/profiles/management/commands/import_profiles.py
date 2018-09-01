from django.core.management.base import BaseCommand
from bdn.course.models import Course
from bdn.provider.models import Provider
from bdn.skill.models import Skill
from bdn.industry.models import Industry
from bdn.company.models import Company
from bdn.certificate.models import Certificate
from bdn.job.models import Job
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
        countLearners = 10
        countBusinesses = 10
        countAcademies = 10
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
                if int(profile) < int(countLearners) and countLearners > 0:
                    profile_obj = Profile.objects.get(user=user)
                    profile_obj.active_profile_type = 1
                    profile_obj.first_name = faker.name().split()[0]
                    profile_obj.last_name = faker.name().split()[1]
                    profile_obj.learner_email = faker.email()
                    profile_obj.learner_position = faker.job()
                    profile_obj.learner_specialisation = "Specialization ..."
                    profile_obj.learner_about = faker.text()
                    profile_obj.learner_country = faker.country()
                    nr_certificates = 0
                    if int(max_certificates) > 0:
                        nr_certificates = \
                            int(random_generator.randint(0,
                                int(max_certificates)))
                        for course in range(0, nr_certificates):
                            Certificate.objects.create(
                                holder=user,
                                user_eth_address=eth_wallet,
                                academy_title='Academy ' + faker.company(),
                                course_title='Course title ' + str(course+1),
                                learner_eth_address=eth_wallet,
                                verified=False
                            )
                    profile_obj.save()
                    print('User eth: ' + str(eth_wallet) + ' was created!')
                    if int(nr_certificates) > 0:
                        print('--> Certificates added')
                    countLearners -= 1
                elif int(profile) < (fake_users-int(countAcademies)) and \
                        countBusinesses > 0:
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
                    nr_jobs = 0
                    if int(max_jobs) > 0:
                        industry, _ = Industry.objects.get_or_create(
                            name='Animation')
                        nr_jobs = \
                            int(random_generator.randint(0, int(max_jobs)))
                        for job in range(0, nr_jobs):
                            job_obj = Job.objects.create(
                                company=company,
                                title=faker.job(),
                                location='Remote',
                                overview=faker.text(),
                                description=faker.text(),
                                hours='12',
                                languages=['English']
                            )
                            job_obj.industries.add(industry)
                            nr_skills = \
                                int(random_generator.randint(1, len(SKILLS)))
                            for skill_id in range(1, nr_skills):
                                skill, _ = Skill.objects.get_or_create(
                                    name=SKILLS[skill_id]
                                )
                                job_obj.skills.add(skill)
                    business_obj.save()
                    print('Business eth: ' + str(eth_wallet) + ' was created!')
                    if nr_jobs > 0:
                        print('--> Jobs added')
                    countBusinesses -= 1
                elif int(profile) < fake_users and countAcademies > 0:
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
                    nr_courses = 0
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
                    countAcademies -= 1
            except Exception:
                continue
        print('Generation of face profiles finished successfully!')
        print(str(Profile.objects.count()) + ' profiles stored in the DB')
        return
