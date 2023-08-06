from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sumdf',
    packages=find_packages(),
    include_package_data=True,
    version='0.1.0',
    license='MIT',
    install_requires=[
        'numpy',
        'pandas',
        'seaborn',
        'tqdm',
        'attrdict',
        'colorlog',
        'six',
    ],
    author='Nariaki Tateiwa',
    author_email='nariaki3551@gmail.com',
    description='Summary of dataframes',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='dataframe',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
)
