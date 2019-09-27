import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pysomq",
    use_scm_version={"write_to": "pysomq/_version.py"},
    setup_requires=["setuptools-scm", "setuptools>=40.0"],
    author="Carsten Sauerbrey",
    author_email="carsten.sauerbrey@gmail.com",
    description="Provide a bidirectional connection to a serial interface via zeroMQ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/casabre/pysomq",
    package_dir={"": "pysomq"},
    install_requires=['pyzmq>=18.1.0', 'pyserial>=3.4'],
    license='MIT',
    platforms=["linux", "win32"],
    classifiers=[
        'Development Status :: 4 - Beta',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
