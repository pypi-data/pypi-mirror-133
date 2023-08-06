from setuptools import setup, find_packages

with open("README.TXT", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sqlite3View",
    version="0.0.1",
    long_description=long_description,
    url="https://github.com/KOMILJONOV/SqliteView",
    author="Komiljonov Shukururullox",
    author_email="komiljonovshukurullox@gmail.com",
    license="MIT",
    keywords="sqlite3 db model models django database",
    packages=find_packages()
)