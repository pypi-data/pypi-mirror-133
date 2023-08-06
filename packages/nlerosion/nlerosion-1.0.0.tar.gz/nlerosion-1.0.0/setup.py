import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nlerosion",
    version="1.0.0",
    author="Mattia de' Michieli Vitturi",
    author_email="demichie@gmail.com",
    description="A python package for nonlinear erosion modeling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/demichie/NLerosion",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ),
)
