#SPDX-License-Identifier: MIT
import io
import os
import re

from setuptools import find_packages
from setuptools import setup
from workers.worker_base import Worker

setup(
	name="libyear_worker",
	version="1.0.0",
	url="https://github.com/ajhenry00/augur",
	license='MIT',
	author="Group6_AndrewGillis_AidanHenry_BenHudson",
	author_email="ajhenry3000@gmail.com",
	description="Augur Worker that gathers the libyear data",
	packages=find_packages(exclude=('tests',)),
	install_requires=[
		'flask',
		'requests',
		'psycopg2-binary',
		'libyear',
	],
    entry_points={
        'console_scripts': [
            'linux_badge_worker_start=workers.linux_badge_worker.runtime:main',
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ]
)
