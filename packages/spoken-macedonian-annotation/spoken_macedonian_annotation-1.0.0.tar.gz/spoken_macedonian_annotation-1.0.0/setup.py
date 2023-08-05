
# -*- coding: utf-8 -*-
# setup.py

# Author: Anastasia Escher
# University of Zurich
# Department of Slavonic linguistics and literatures


import setuptools

with open('README.md', 'r') as readme:
    long_description = readme.read()

setuptools.setup(
    name='spoken_macedonian_annotation',
    version='1.0.0',
    author='Anastasia Escher',
    description='Library and CLI to for simple morphological annotation of spoken Macedonian',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        'nltk>=3.4.5'
    ],
    entry_points={
        'console_scripts': [
            'annotateMac = spoken_macedonian_annotation.cli:main'
        ]
    },
    include_package_data=True,
    package_data={'spoken_macedonian_annotation': ['all_data.json']}
    )


