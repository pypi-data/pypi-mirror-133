import setuptools
from pathlib import Path

setuptools.setup(
    name="mikemorris101pdf",
    version=1.0,
    setup_requires=['wheel'],
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(
        exclude=["test", "data"])  # exclude test and data
)

# py setup.py sdist bdist_wheel
