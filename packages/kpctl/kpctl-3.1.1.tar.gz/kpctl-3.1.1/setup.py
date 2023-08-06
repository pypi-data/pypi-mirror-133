import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="kpctl",
    version="3.1.1",
    description="Command line interface for managing and executing BPMN",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/tstephen/bpaas",
    author="KnowProcess",
    author_email="info@knowprocess.com",
    license="Apache",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
    ],
    packages=["kpctl"],
    include_package_data=True,
    install_requires=["cairosvg", "oauthlib", "requests", "requests_oauthlib"],
    entry_points={
        "console_scripts": [
            "kpctl=kpctl.__main__:main",
        ]
    },
)

