from setuptools import setup, find_packages


setup(
    name='financials',
    url='http://pypi.python.org/pypi/financials/',
    version = 1.5,
    author='cmmeyer1800',
    author_email='collinmmeyer@gmail.com    ',
    python_requires = ">=3.6",
    long_description=open('README.md').read(),
    packages= find_packages(
        where='src'
    ),
    package_dir={'': 'src'},
    install_requires=[
        "openpyxl>=3.0.9",
        "python-dateutil>=2.8.2",
        "requests>=2.27.1",
        "tk>=0.1.0"
    ]
)