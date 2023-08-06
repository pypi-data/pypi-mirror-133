import pip
from setuptools import setup, find_packages

__version__ = "0.0.1"

with open("README.md") as f:
    readme = f.read()

setup(
    name="pxpip",
    version=__version__,
    description="A Proxy wrapper around pip to enable cloud interfaces without the need for pipy",
    long_description=readme,
    author="claytonbezuidenhout",
    url="https://github.com/claytonbezuidenhout/pxpip",
    packages=find_packages(exclude=("tests", "dist", "docker", "venv")),
    install_requires=[
        "boto3==1.20.26"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.8",
)
