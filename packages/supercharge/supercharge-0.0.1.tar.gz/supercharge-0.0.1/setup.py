import pathlib

import setuptools

long_description = pathlib.Path("README.rst").read_text()

setuptools.setup(
    name="supercharge",
    version="0.0.1",
    author="zincwarecode",
    author_email="zincwarecode@gmail.com",
    description="Expand Python Super Capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zincware/supercharge",
    download_url="https://github.com/zincware/supercharge/archive/beta.tar.gz",
    keywords=["super", "inheritance", "ZnTrack"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Eclipse Public License 2.0 (EPL-2.0)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
