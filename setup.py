from setuptools import setup, find_packages
from os import path, walk

setup(
    name='PyTreasuryDirect',
    version='0.1.0',
    zip_safe = True,
    packages=find_packages(),
    license='',
    author='Nicholas Pezolano',
    author_email='npezolano@gmail.com',
    description='A Python wrapper for the Treasury Direct API',
    install_requires=['requests'],
)