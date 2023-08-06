import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-Matrix-123",
    version="0.0.2",
    author="Robed Beauvile",
    author_email="robedbeauvil@gmail.com",
    description="A python package that retrieves matrix dimensions, their trace, and performs matrix addition, subtraction, multiplication.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/beauvilerobed/py-matrix-123",
    packages=setuptools.find_packages()
)