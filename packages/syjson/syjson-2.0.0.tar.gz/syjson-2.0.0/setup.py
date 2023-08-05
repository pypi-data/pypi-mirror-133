import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="syjson",
    version="2.0.0",
    author="DomySh",
    author_email="me@domysh.com",
    install_requires=["pybson"],
    description="A library for manage jsons files as dicts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DomySh/syjson",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
