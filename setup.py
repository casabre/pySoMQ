import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pySoMQ",
    version="0.0.1",
    author="Carsten Sauerbrey",
    author_email="carsten.sauerbrey@gmail.com",
    description="Provide a bidirectional connection to a serial interface via zeroMQ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/casabre/pysomq",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)