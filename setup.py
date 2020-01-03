import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="prometheus-api-client",
    version="0.2.0",
    author="Anand Sanmukhani",
    author_email="asanmukh@redhat.com",
    description="A small python api to collect data from prometheus",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AICoE/prometheus-api-client-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
