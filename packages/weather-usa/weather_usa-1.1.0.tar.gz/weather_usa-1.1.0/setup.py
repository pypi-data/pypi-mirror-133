import pathlib
from setuptools import setup, find_packages

CURRENT_DIRECTORY = pathlib.Path(__file__).parent

# The text of the README file
README = (CURRENT_DIRECTORY / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="weather_usa",
    version="1.1.0",
    description="Wrapper for parts of the IEM and NWS API, built with asyncio for speed",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Shom770/weather_usa",
    license="MIT",
    install_requires=["aiohttp", "inflection"],
    packages=find_packages()
)