import os

import setuptools

NAME = 'sm_icon_extractor'

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name = 'sm-icon-extractor',
    version = '1.0.0',
    author = 'EV3R4',
    author_email = 'ever@brokenmouse.studio',
    description = 'Extracts icons from Scrap Mechanic.',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://git.brokenmouse.studio/ever/sm-icon-extractor',
    packages = setuptools.find_packages(),
    classifiers = [
        'License :: OSI Approved :: BSD License',
        
        'Programming Language :: Python :: 3',
        
        'Operating System :: OS Independent',
    ],
    install_requires = ['Pillow'],
    python_requires = '>=3.9',
    entry_points={
        'console_scripts': [
            'sm-icon-extractor=sm_icon_extractor.__main__:main',
        ],
    },
)
