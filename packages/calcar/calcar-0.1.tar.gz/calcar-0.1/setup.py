from setuptools import setup, find_packages


setup(
    name="calcar",
    version="0.1",
    description="This is a Python Package which will help you to calculate two numbers!",
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    license="MIT License",
    author="Arinjoy Nath",
    author_email="arinjoy762@gmail.com",
    keywords='calculator',
    packages=find_packages(),
    install_requires=['']
)