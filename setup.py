from setuptools import setup, find_packages
from os import path, walk

setup(
    name='PyTreasuryDirect',
    version='0.1.1',
    zip_safe = True,
    packages=find_packages(),
    license='MIT',
    author='Nicholas Pezolano',
    author_email='npezolano@gmail.com',
    description='A Python wrapper for the Treasury Direct API',
    url='https://github.com/npezolano/PyTreasuryDirect',
    install_requires=['requests'],
)
