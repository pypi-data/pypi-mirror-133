from setuptools import setup
from setuptools import find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fzip",
    version="0.0.3",
    author="Johnny Rocha",
    author_email="johnny.devcode@gmail.com",
    description="package to cep requests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JohnnyDev2001/fast_zipcode",
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"fzip": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9",
)