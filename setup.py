import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="altFACS",                          #100% required
    version="1.0.8",                         #100% required
    description="FACS tools for split fluorescent proteins",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/BoHuangLab/altFACS",
    author="David Brown",
    author_email="david.brown3@ucsf.edu",
    license="MIT",
    classifiers=[
        #"License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"],
    packages=["altFACS"],                    #100% required
    include_package_data=True,
    install_requires=["fcsparser",
        "numpy",
        "pandas",
        "matplotlib",
        "pickleshare",
        "scipy"]
)
