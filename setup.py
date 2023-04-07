from setuptools import setup, find_packages
from hentaila.__vars__ import __version__, __author__, __email__


setup(
    name='hentaila',
    version=__version__,
    packages=find_packages(),
    url='https://github.com/TaprisSugarbell/hentaila',
    author=__author__,
    author_email=__email__,
    description='Unofficial https://www3.hentaila.com/ Package',
    long_description=open("./README.md", "r").read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "beautifulsoup4",
        "cloudscraper"
    ],
    project_urls={
        "Issue tracker": "https://github.com/TaprisSugarbell/hentaila/issues"
    }
)
