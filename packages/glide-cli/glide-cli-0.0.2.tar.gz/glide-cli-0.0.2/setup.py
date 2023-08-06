from setuptools import setup

setup(
        name="glide-cli",
    version='0.0.2',
    py_modules=['src.cli'],
    install_requires=[
        'Click',
        'tabulate'
    ],
    entry_points='''
        [console_scripts]
        glide=src.cli:cli
    ''',
)
