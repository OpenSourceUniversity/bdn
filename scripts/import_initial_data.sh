#!/bin/bash

echo "Starting import of categories..."
python manage.py import_categories
CATEGORIES_IMPORTED=$?
if [ $CATEGORIES_IMPORTED -eq 0 ];then
   echo "Categories successfully imported."
else
   echo "Categories import failed."
   exit 1
fi
