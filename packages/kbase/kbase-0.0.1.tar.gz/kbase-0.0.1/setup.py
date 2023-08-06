from setuptools import setup, find_packages
import codecs
import os
from pip._internal.req import parse_requirements


VERSION = '0.0.1'
DESCRIPTION = 'kbase'
LONG_DESCRIPTION = 'A package automation operations'
REQUIREMENTS = parse_requirements('requirements.txt', session=False)

# Setting up
setup(
    name="kbase",
    version=VERSION,
    author="Jebin Jolly Abraham",
    author_email="jebinjabraham@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_reqs = REQUIREMENTS,
    keywords=['jebin', 'jabraham', 'kbase', 'automation', 'python', 'package', 'manager'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

