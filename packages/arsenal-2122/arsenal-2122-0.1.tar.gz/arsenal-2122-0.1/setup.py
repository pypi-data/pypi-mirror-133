from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='arsenal-2122',
    version='0.1',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages()
)
