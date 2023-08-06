from setuptools import setup, find_packages

setup(
        name="glide-cli",
    version='0.1.1',
    install_requires=[
        'Click',
        'tabulate'
    ],
    packages=["src"],
    entry_points='''
        [console_scripts]
        glide=src.cli:cli
    ''',
)
