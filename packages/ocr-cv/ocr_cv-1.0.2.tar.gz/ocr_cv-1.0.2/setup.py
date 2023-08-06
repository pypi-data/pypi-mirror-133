from setuptools import setup, find_packages

setup(
    name='ocr_cv',
    version='1.0.2',
    description='Generate keywords from CVs',
    author='Gal Ben Haim',
    author_email='galbhmusic@gmail.com',
    license='MIT',
    packages=find_packages(include=['ocr_cv']),
    url='https://gitlab.com/galbh/ocr',
    zip_safe=False
)
