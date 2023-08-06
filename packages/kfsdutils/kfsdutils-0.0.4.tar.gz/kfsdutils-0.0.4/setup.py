from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='kfsdutils',
      version='0.0.4',
      description='Sample Pkg',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='nathangokul',
      packages=find_packages(),
      zip_safe=False,
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)
