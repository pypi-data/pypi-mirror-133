
# Import packages
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="superstocks",
    version="0.0.1",
    author="Kumar Nityan Suman",
    author_email="nityan.suman@gmail.com",
    description="Unified AI trading platform powered by human intelligence.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "superstocks"},
    packages=setuptools.find_packages(where="superstocks"),
    python_requires=">=3.8",
)
