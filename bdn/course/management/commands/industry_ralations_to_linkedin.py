from django.core.management.base import BaseCommand


class LinkedinIndustryRelation(BaseCommand):
    ''' Industry relation between LinkedIn and all other providers '''
    def __init__(self):
        self.subject_industry = {
            'k12': [
                'Social Sciences',
                'Professional Training & Coaching',
                'Primary/Secondary Education',
                'Higher Education'],
            'psychology': [
                'Social Sciences',
                'Higher Education',
                'Health, Wellness and Fitness'],
            'management & leadership': [
                'Management Consulting',
                'Education Management'],
            'test prep': ['Higher Education'],
            'religion': ['Religion'],
            'music': ['Music', 'Fine Art'],
            'political science': [
                'Social Sciences',
                'Political Organization'],
            'social sciences': ['Financial Services'],
            'public & global health': [
                'Health',
                'Wellness and Fitness'],
            'civil & environmental engineering': [
                'Mechanical or Industrial Engineering',
                'Civil Engineering'],
            'literature': [
                'Language & Culture',
                'Primary/Secondary Education',
                'Higher Education'],
            'finance': ['Accounting', 'Banking', 'Financial Services'],
            'statistics & probability': [
                'Mathematics',
                'Primary/Secondary Education',
                'Higher Education'],
            'philosophy': ['Social Sciences', 'Higher Education'],
            'entrepreneurship': [
                'Venture Capital & Private Equity',
                'Capital Markets'],
            'anthropology': ['Social Sciences'],
            'bioinformatics': ['Biotechnology'],
            'web development': ['Computer Software'],
            'nutrition & wellness': ['Health, Wellness and Fitness'],
            'higher education': ['Higher Education'],
            'grammar & writing': ['Writing and Editing'],
            'art & design': ['Design'],
            'course development': [
                'Primary/Secondary Education',
                'Higher Education',
                'Education Management',
                'E-Learning'],
            'disease & disorders': [
                'Mental Health Care',
                'Hospital & Health Care',
                'Health, Wellness and Fitness'],
            'business development': ['Management Consulting'],
            'algebra & geometry': ['Mathematics'],
            'history': [
                'Social Sciences',
                'Primary/Secondary Education',
                'Higher Education'],
            'astronomy': ['Science'],
            'electrical engineering': ['Telecommunications'],
            'sociology': ['Social Sciences'],
            'stem': ['Research'],
            'calculus & mathematical analysis': ['Mathematics'],
            'teacher development': ['Higher Education'],
            'theoretical computer science': ['Computer Software'],
            'biology': ['Science'],
            'health care & research': [
                'Medical Practice',
                'Hospital & Health Care',
                'Health, Wellness and Fitness'],
            'digital media & video games': [
                'Online Media',
                'Media Production',
                'Broadcast Media',
                'Entertainment',
                'Design',
                'Computer Games'],
            'language & culture': ['Language & Culture'],
            'foundations of mathematics': [
                'Social Sciences',
                'Mathematics',
                'Primary/Secondary Education'],
            'law': ['Social Sciences', 'Law Practice'],
            'mobile development': ['Computer Software'],
            'environmental science': ['Science',
                                      'Renewables & Environment',
                                      'Environmental Services'],
            'economics': ['Social Sciences',
                          'Primary/Secondary Education',
                          'Accounting',
                          'Banking',
                          'Financial Services'],
            'programming': ['Computer Software'],
            'databases': ['Computer Software'],
            'chemistry': ['Science', 'Chemicals'],
            'physics': [
                'Science',
                'Primary/Secondary Education',
                'Higher Education'],
            'data science and big data': ['Science', 'Computer Software'],
            'visual arts': ['Animation', 'Arts and Crafts'],
            'mechanical engineering': [
                'Mechanical or Industrial Engineering',
                'Consumer Electronics',
                'Electrical/Electronic Manufacturing'],
            'online education': ['E-Learning'],
            'film & theatre': ['Motion Pictures and Film', 'Fine Art'],
            'professional development': [
                'Public Relations and Communications',
                'Program Development'],
            'marketing': [
                'Social Sciences',
                'Public Relations and Communications',
                'Marketing and Advertising'],
            'artificial intelligence': ['Computer Software']
        }

    def class_central(self, subject):
        try:
            result = self.subject_industry[subject.lower()]
        except Exception:
            result = []
        return result
