"""
Basic setup for project
"""
import os

from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, 'README.md')) as f:
    README = f.read()

BASE = 'eventer/' if os.path.isdir(os.path.join(HERE, 'eventer')) else ''

PREQ = os.path.join(HERE, BASE + "requirements.txt")
PREQ_DEV = os.path.join(HERE, BASE + "requirements-dev.txt")

setup(
    name='eventer',
    version='1.0.0',
    description='tacoma-eventer',
    long_description=README,
    classifiers=[
        "Programming Language :: Python",
    ],
    author='Nick LaPierre',
    author_email='nlapierre@infoblox.com',
    url='sweester.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[i.strip() for i in open(PREQ).readlines()],
    tests_require=[i.strip() for i in open(PREQ_DEV).readlines()],
    test_suite="tests",
    entry_points="",
)
