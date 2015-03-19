from setuptools import setup, find_packages

def read(filename):
    with open(filename) as f:
        return f.read()

setup(
    name="pio",
    version=read("VERSION"),
    description='A scale-out IO benchmarking framework',
    long_description=read("README.md"),
    license='Apache License 2.0',

    author='Irad Cohen',
    author_email='irad.cohen@sap.com',

    install_requires=[
        'ClusterShell'],

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],

    packages=find_packages(),
    include_package_data = True,

    entry_points={
        'console_scripts': ['pio=pio.pio:main']
    }
)

