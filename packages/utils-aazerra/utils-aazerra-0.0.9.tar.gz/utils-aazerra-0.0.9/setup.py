from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='utils-aazerra',
    version='0.0.9',
    packages=find_packages(exclude=["tests"]),
    url='https://github.com/Aazerra/utils',
    license='MIT',
    author='Alireza Rabie',
    author_email='alirezarabie793@gmail.com',
    description='A bunch of utils function for personal use',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
