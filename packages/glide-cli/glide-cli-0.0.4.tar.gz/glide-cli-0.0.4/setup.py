from setuptools import setup, find_packages

setup(
        name="glide-cli",
    version='0.0.4',
    install_requires=[
        'Click',
        'tabulate'
    ],
    packages=find_packages(exclude=("tests",)),
    entry_points='''
        [console_scripts]
        glide=src.cli:cli
    ''',
)
