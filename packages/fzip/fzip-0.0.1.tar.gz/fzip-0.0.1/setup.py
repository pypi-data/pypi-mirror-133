import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fzip",
    version="0.0.1",
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
    package_dir={"fzip": "./fzip"},
    packages=setuptools.find_packages(where="fzip"),
    python_requires=">=3.9",
)