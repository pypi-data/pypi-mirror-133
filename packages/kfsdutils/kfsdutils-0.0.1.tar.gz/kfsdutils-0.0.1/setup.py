import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kfsdutils",
    version="0.0.1",
    author="nathangokul",
    author_email="nathangokul111@gmail.com",
    description="Sample Pkg",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "kfsdutils"},
    packages=setuptools.find_packages(where="kfsdutils"),
    python_requires=">=3.6",
)
