import setuptools

with open("README.txt", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydevpack", # Replace with your own PyPI username(id)
    version="0.0.3",
    author="Jeong Woobin",
    author_email="battlegom@outlook.kr",
    description="pycalc, pytime module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sh901soft",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)