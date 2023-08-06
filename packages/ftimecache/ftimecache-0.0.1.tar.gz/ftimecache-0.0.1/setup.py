from setuptools import setup
from pathlib import Path

README = (Path(__file__).parent / "README.md").read_text()

setup(
    name="ftimecache",
    version="0.0.1",
    description="Decorator to cache function return values based on time.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Dimfred/ftimecache",
    author="dimfred",
    author_email="dimfred.1337@web.de",
    license="MIT",
    classifiers={
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    },
    packages=["ftimecache"],
    include_package_data=True,
)
