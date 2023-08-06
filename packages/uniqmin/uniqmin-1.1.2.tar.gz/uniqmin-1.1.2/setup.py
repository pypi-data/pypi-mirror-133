import pathlib
from setuptools import setup

VERSION = '1.1.2'
DESCRIPTION = 'An alignment-independent tool for the study of pathogen sequence diversity at any given rank of taxonomy lineage'

HERE = pathlib.Path(__file__).parent
README = (HERE/ "README.md").read_text()

setup(
    name='uniqmin',
    version=VERSION,
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    author="Chong LC",
    author_email="<lichuinchong@gmail.com>",
    keywords=("pathogen, sequence diversity, alignment-independent"),
    project_urls = 
      {"Github": "https://github.com/ChongLC/MinimalSetofViralPeptidome-UNIQmin"},
    packages=["uniqmin"],
    install_requires=['biopython', 'pandas', 'pyahocorasick'],
    entry_points={
        "console_scripts": [
            "uniqmin=uniqmin.__main__:main",
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "License :: OSI Approved :: MIT License", 
        "Natural Language :: English",
        
    ]
)

