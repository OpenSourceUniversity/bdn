#!/bin/bash

echo "Starting import of industries..."
python manage.py import_industries
INDUSTRIES_IMPORTED=$?
if [ $INDUSTRIES_IMPORTED -eq 0 ];then
   echo "Industries successfully imported."
else
   echo "Industries import failed."
   exit 1
fi

echo "Starting import of standardized skills..."
python manage.py import_standardized_skills
SKILLS_IMPORTED=$?
if [ $SKILLS_IMPORTED -eq 0 ];then
   echo "Skills successfully imported."
else
   echo "Skills import failed."
   exit 1
fi

echo "Starting import of courses..."
python manage.py import_courses --file="data/courses/Art _ Design.json" --industry="Design"
python manage.py import_courses --file="data/courses/Business.json" --industry="Management Consulting"
python manage.py import_courses --file="data/courses/Computer Science.json" --industry="Computer & Network Security"
python manage.py import_courses --file="data/courses/Data Science.json" --industry="Information Technology and Services"
python manage.py import_courses --file="data/courses/Education _ Teaching.json" --industry="Higher Education"
python manage.py import_courses --file="data/courses/Engineering.json" --industry="Mechanical or Industrial Engineering"
python manage.py import_courses --file="data/courses/Health _ Medicine.json" --industry="Health, Wellness and Fitness"
python manage.py import_courses --file="data/courses/Humanities.json" --industry="Civic & Social Organization"
python manage.py import_courses --file="data/courses/Mathematics.json"
python manage.py import_courses --file="data/courses/Personal Development.json"
python manage.py import_courses --file="data/courses/Programming.json"
python manage.py import_courses --file="data/courses/Science.json"
python manage.py import_courses --file="data/courses/Social Sciences.json" --industry="Civic & Social Organization"
