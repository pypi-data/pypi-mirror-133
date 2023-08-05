from setuptools import setup


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fzip",
    version="0.0.2",
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
    python_requires=">=3.9",
)