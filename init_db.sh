#!/usr/bin/env bash


python manage.py makemigrations
python manage.py migrate


#python manage.py loaddata author_detail.json   # 先author_detail，再author（两者有一对一关联）
#python manage.py loaddata author.json