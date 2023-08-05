import setuptools
from pathlib import Path

setuptools.setup(
    name="rachealpdf",
    version=1.1,
    lond_description=Path("README.MD").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])


)
