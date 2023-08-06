import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="parseUALF",  # Replace with your own username
    version="0.0.1",
    author="Hilde Haland",
    author_email="hilde.tveit.haland@gmail.com",
    description="Python class that allows for a python requests response received in the universal ascii lightning "
                "format to be parsed to a pandas dataframe object.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hildeha/UAFL_dataframe_parser",
    packages=setuptools.find_namespace_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests>=2.26.0",
        "pandas>=1.0.0",
        "numpy>=1.0.0",
        "plotly>=5.2.1"
    ]
)
