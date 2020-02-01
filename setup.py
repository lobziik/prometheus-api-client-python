import setuptools
import os
import re

with open("README.md", "r") as fh:
    long_description = fh.read()

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))


def get_version():
    with open(os.path.join(ROOT_DIR, "prometheus_api_client", "__init__.py")) as fd:
        content = fd.read()
        version = re.findall(r'__version__ = "(.+)"', content)[0]
        print(version)
        return version


setuptools.setup(
    name="prometheus-api-client",
    version=get_version(),
    author="Anand Sanmukhani",
    author_email="asanmukh@redhat.com",
    description="A small python api to collect data from prometheus",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AICoE/prometheus-api-client-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
