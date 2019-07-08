# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from micro_django_demo.settings import MICRO_VERSION

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

install_packages = []

with open('requirements.txt') as f:
    while True:
        line = f.readline()
        if not line:
            break
        line = line.strip('\n')
        install_packages.append(line)


setup(
    name='micro-django-demo',
    version=MICRO_VERSION,

    description='Sample package for Python-Guide.org',
    long_description=readme,
    author='DancingSnow',
    author_email='dancinginmysnow@gmail.com',
    url='https://github.com/dancingsnow/micro-django-demo',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    package_data = {
            'micro-django-demo':['*.html']
        },
    install_requires=install_packages,
    entry_points={
        'console_scripts': [
            'micro-django-start=micro_django_demo.entry:main',
        ]
    }
)