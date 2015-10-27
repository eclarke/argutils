from setuptools import setup, find_packages

with open("VERSION") as version_file:
    version = version_file.read().strip()

setup(
    name="argutils",
    packages=find_packages(),
    version=version,
    author='Erik Clarke',
    author_email='ecl@mail.med.upenn.edu',
    url='https://github.com/eclarke/argutils',
    description='Utilities to convert argument lists to parsers and config files',
    install_requires=[
    	'six'
    ]
)
