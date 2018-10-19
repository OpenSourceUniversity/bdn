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
python manage.py import_courses
