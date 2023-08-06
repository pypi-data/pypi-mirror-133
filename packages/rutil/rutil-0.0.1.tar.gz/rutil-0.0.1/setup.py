from setuptools import find_packages, setup

base_dependencies = [
    "pandas>=1.0.0",
    "python-dateutil>=2",
]


additional_dependencies = {
    "dev": ["black>=21.9b0", "pre-commit>=2.15.0", "pytest>=6.2.1", "pylint>=2.7.4", "jupyterlab"],
}

VERSION = "0.0.1"
DESCRIPTION = "R original utilities now in python"
LONG_DESCRIPTION = """
    The idea of this package is to translate useful R functions into python
    The first implementation is the R str() function to show the structure of pandas dataframes

    """


setup(
    name="rutil",
    packages=find_packages(where="rutil"),
    package_dir={"": "rutil"},
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Ismael Cabral",
    version="0.0.1",
    py_modules=["rutil"],
    keywords= ["R language", "R","str()","pandas","struture"],
    install_requires=base_dependencies,
    extras_require=additional_dependencies,
)


