from distutils.core import setup
import setuptools
from os.path import join

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='nifti_snapshot',
    version='v0.1.3',
    description='First release to test pypi',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='kcho',
    author_email='kevincho@bwh.harvard.edu',
    url='https://github.com/pnlbwh/nifti-snapshot',
    download_url='https://github.com/pnlbwh/nifti-snapshot/archive/refs/tags/nifti-snapshot.zip',
    keywords=['nifti', 'snapshot'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.7',
    scripts=['scripts/nifti_snapshot']
)
